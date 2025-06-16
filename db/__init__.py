import os
from dotenv import load_dotenv
import pyodbc

load_dotenv()  # Carrega as variáveis do .env

conn_str = os.getenv("DB_CONN_STR")

def get_connection():
    try:
        conn =  pyodbc.connect(conn_str)
        print("Conexão bem-sucedida!")
        return conn
    except Exception as e:
        print(f"Erro ao conectar: {e}")
        
