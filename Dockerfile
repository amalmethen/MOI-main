FROM python:3.11.8-bullseye

# Copy the application code and install dependencies
COPY . /src
WORKDIR /src

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

EXPOSE 8000

# Run the FastAPI application with Uvicorn
CMD ["uvicorn", "pacifastapi:app", "--host", "0.0.0.0", "--port", "8000"]
