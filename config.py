import os
from dotenv import load_dotenv
import urllib.parse

load_dotenv()

class Config: 
    SQL_DRIVER = os.getenv('AZURE_SQL_DRIVER')
    SQL_SERVER = os.getenv('AZURE_SQL_SERVER')
    SQL_DATABASE = os.getenv('AZURE_SQL_DATABASE')
    SQL_ENCRYPT = os.getenv('AZURE_SQL_ENCRYPT')
    SQL_TRUST_CERTIFICATE = os.getenv('AZURE_SQL_TRUST_CERTIFICATE')
    SQL_CONNECTION_TIMEOUT = os.getenv('AZURE_SQL_CONNECTION_TIMEOUT') 

    def get_database_uri():
        connection_string  = (
            f"Driver={os.getenv('AZURE_SQL_DRIVER')};"
            f"Server={os.getenv('AZURE_SQL_SERVER')};"
            f"Database={os.getenv('AZURE_SQL_DATABASE')};"
            f"Encrypt={os.getenv('AZURE_SQL_ENCRYPT')};"
            f"TrustServerCertificate={os.getenv('AZURE_SQL_TRUST_CERTIFICATE')};"
            f"Connection Timeout={os.getenv('AZURE_SQL_CONNECTION_TIMEOUT')};"
        )
        return connection_string 