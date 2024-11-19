import os
import pyodbc, struct
from azure import identity

from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel

class CareGiver(BaseModel):
    caregive_id: str
connection_string = 'Driver={ODBC Driver 18 for SQL Server};Server=tcp:deass.database.windows.net,1433;Database=medication;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30'

app = FastAPI()

@app.get("/")
def root():
    print("START")
    return "SQL DATABASE"

@app.get("/all")
def get_care_giver():
    rows = []
    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM [dbo].[caregiver]")

        for row in cursor.fetchall():
            rows.append(f"{row.caregiver_id}")
    return rows

@app.get("/caregiver/{caregiver_id}")
def get_person(caregiver_id: int):
    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM [dbo].[caregiver] WHERE caregiver_id = ?", caregiver_id)

        row = cursor.fetchone()
        return f"{row.caregiver_id}"

# @app.post("/person")
# def create_person(item: Person):
#     with get_conn() as conn:
#         cursor = conn.cursor()
#         cursor.execute(f"INSERT INTO Persons (FirstName, LastName) VALUES (?, ?)", item.first_name, item.last_name)
#         conn.commit()

#     return item

def get_conn():
    credential = identity.DefaultAzureCredential(exclude_interactive_browser_credential=False)
    token_bytes = credential.get_token("https://database.windows.net/.default").token.encode("UTF-16-LE")
    token_struct = struct.pack(f'<I{len(token_bytes)}s', len(token_bytes), token_bytes)
    SQL_COPT_SS_ACCESS_TOKEN = 1256  # This connection option is defined by microsoft in msodbcsql.h
    conn = pyodbc.connect(connection_string, attrs_before={SQL_COPT_SS_ACCESS_TOKEN: token_struct})
    return conn