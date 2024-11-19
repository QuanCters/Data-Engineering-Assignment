from flask import Flask
from flask_restx import Api
import pyodbc, struct
from azure import identity
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
import urllib
from config import Config

api = Api(
title="Flask API with Azure SQL",
version="1.0",
description="API documentation"
)

def get_engine():
    # Acquire Azure AD Access Token
    credential = identity.DefaultAzureCredential(exclude_interactive_browser_credential=False)
    access_token = credential.get_token("https://database.windows.net/.default").token

    # Encode the access token in UTF-16LE as required by pyodbc
    access_token_bytes = access_token.encode("UTF-16LE")
    token_struct = struct.pack('<I', len(access_token_bytes)) + access_token_bytes

    # Define the ODBC connection string without Authentication, Integrated Security, User, or Password
  
    connection_string = Config.get_database_uri()

    # URL-encode the connection string
    odbc_connection_string = urllib.parse.quote_plus(connection_string)

    # Create the SQLAlchemy Engine with the access token
    engine = create_engine(
        f"mssql+pyodbc:///?odbc_connect={odbc_connection_string}",
        connect_args={
            'attrs_before': {1256: token_struct}  # SQL_COPT_SS_ACCESS_TOKEN
        },
        poolclass=NullPool  # Disable connection pooling
    )

    return engine

def create_app():
    app = Flask(__name__)
    api.init_app(app)

    with app.app_context():
        from app.routes import caregiver_ns
        api.add_namespace(caregiver_ns, path='/caregivers')
    

    return app  

