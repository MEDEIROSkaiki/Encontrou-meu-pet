import os
from dotenv import load_dotenv
import pyodbc

load_dotenv()  # Carrega as variáveis do .env

conn_str = os.getenv("DB_CONN_STR")

def get_connection():
    return pyodbc.connect(conn_str)
