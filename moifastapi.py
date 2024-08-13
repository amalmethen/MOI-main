import os
import ibm_db
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Any
from ibm_watson_machine_learning.foundation_models import Model
from ibm_watson_machine_learning.metanames import GenTextParamsMetaNames as GenParams
from langchain.prompts import PromptTemplate
from langchain.chains import create_sql_query_chain
import prompt_util

app = FastAPI()

# Load environment variables from creds.env
load_dotenv('/path/to/creds.env')

api_key = os.getenv("API_KEY")
ibm_cloud_url = os.getenv("IBM_CLOUD_URL")
project_id = os.getenv("PROJECT_ID")
uid = os.getenv("DB_USER_ID")
pwd = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOSTNAME")
port = os.getenv("DB_PORT")
database = os.getenv("DB_NAME")
ssl_certificate = os.getenv("SSL_CERTIFICATE_PATH")

if not all([api_key, ibm_cloud_url, project_id, uid, pwd, host, port, database, ssl_certificate]):
    raise Exception("Ensure all necessary environment variables are set")

creds = {
    "url": ibm_cloud_url,
    "apikey": api_key 
}

def send_to_watsonxai(prompts, model_name="codellama/codellama-34b-instruct-hf",
                      decoding_method="greedy", max_new_tokens=100,
                      min_new_tokens=30, temperature=1.0, repetition_penalty=1.0):
    assert not any(map(lambda prompt: len(prompt) < 1, prompts)), "Prompts cannot be empty"

    model_params = {
        GenParams.DECODING_METHOD: decoding_method,
        GenParams.MIN_NEW_TOKENS: min_new_tokens,
        GenParams.MAX_NEW_TOKENS: max_new_tokens,
        GenParams.STOP_SEQUENCES: [";"],
        GenParams.REPETITION_PENALTY: repetition_penalty,
    }

    model = Model(model_id=model_name, params=model_params, credentials=creds, project_id=project_id)
    llm_responses = []
    for prompt in prompts:
        llm_response = model.generate_text(prompt)
        llm_responses.append(llm_response)

    return llm_responses

command_ = prompt_util.command
references_ = prompt_util.references
schema_ = prompt_util.schema
notes_ = prompt_util.notes
examples_ = prompt_util.examples
request_ = "How many residency certificates are currently active?"

pattern = """{command}
    Schema: {schema} 
    References: {references}
    {examples}
    Input: {request}
    Output: """
prompt_template = PromptTemplate.from_template(pattern)

prompt = prompt_template.format(command=command_, schema=schema_, references=references_, examples=examples_, notes=notes_, request=request_)

def db_connection():
    db2_dsn = (
        f"DATABASE={database};"
        f"HOSTNAME={host};"
        f"PORT={port};"
        f"PROTOCOL=TCPIP;"
        f"UID={uid};"
        f"PWD={pwd};"
        f"SECURITY=SSL;"
        f"SSLServerCertificate={ssl_certificate}"
    )
    return ibm_db.connect(db2_dsn, "", "")

class InputText(BaseModel):
    text: str

class ProcessedText(BaseModel):
    results: Any

@app.post("/process/", response_model=ProcessedText)
def process(input_text: InputText):
    data = input_text.text
    if data:
        prompt = prompt_template.format(command=command_, schema=schema_, references=references_, examples=examples_, notes=notes_, request=data)
        response = send_to_watsonxai(prompts=[prompt])
        connection = db_connection()
        stmt = ibm_db.exec_immediate(connection, response[0])
        query_results = ibm_db.fetch_tuple(stmt)
        return {"results": query_results}

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    app.run(host='0.0.0.0', port=port)