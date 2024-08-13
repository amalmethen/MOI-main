command = """Your task is to generate SQL queries that will be used to pull data from the TRESIDENCY_CERTIFI_X table in a SQL database. 
The schema for the table is:
"""

schema = """
sql CREATE TABLE TRESIDENCY_CERTIFI_X(
    NUMBER                INTEGER PRIMARY KEY,
    ARTICAL               INTEGER,
    ISSUE_PLACE           VARCHAR(50),
    DATE_OF_ISSUE         DATE,
    REASON_FOR_EXIT       VARCHAR(50),
    STATUS                VARCHAR(20),
    RES_CERT_SEQ_NUM      INTEGER,
    PP_NATIONAL_NUMBER    INTEGER,
    CANCELLATION_REASON   VARCHAR(50),
    CANCELLATION_DATE     DATE,
    PUB_ORG_NUMBER        INTEGER
);
"""

references = """
Possible values for STATUS are 'Active', 'Inactive', 'Cancelled'. No other value is permitted.
Possible values for ISSUE_PLACE and REASON_FOR_EXIT should match the corresponding values found in the database.
"""

notes = """
"""

examples = """
Input: How many residency certificates are currently active?
Output: SELECT COUNT(*) AS "NUMBER OF ACTIVE CERTIFICATES" FROM TRESIDENCY_CERTIFI_X WHERE STATUS = 'Active';

Input: What is the distribution of residency certificates by their issue place?
Output: SELECT ISSUE_PLACE, COUNT(*) AS "NUMBER OF CERTIFICATES" FROM TRESIDENCY_CERTIFI_X GROUP BY ISSUE_PLACE;

Input: Which reason for exit is the most common among residency certificate cancellations?
Output: SELECT REASON_FOR_EXIT, COUNT(*) AS "NUMBER OF CANCELLATIONS" FROM TRESIDENCY_CERTIFI_X WHERE CANCELLATION_DATE IS NOT NULL GROUP BY REASON_FOR_EXIT ORDER BY COUNT(*) DESC LIMIT 1;

Input: What is the average time between the issuance and cancellation of residency certificates?
Output: SELECT AVG(DATEDIFF(day, DATE_OF_ISSUE, CANCELLATION_DATE)) AS "AVERAGE TIME TO CANCELLATION (DAYS)" FROM TRESIDENCY_CERTIFI_X WHERE CANCELLATION_DATE IS NOT NULL;

Input: How many residency certificates were issued under each article?
Output: SELECT ARTICAL, COUNT(*) AS "NUMBER OF CERTIFICATES" FROM TRESIDENCY_CERTIFI_X GROUP BY ARTICAL;
"""
