from flask import Flask
from dotenv import load_dotenv

import os
import rotas
import rotas.api
import rotas.auth
import rotas.main

# Cria uma instância da aplicação Flask
app = Flask(__name__)
load_dotenv() 

# Configure a SECRET_KEY a partir da variável de ambiente
app.secret_key =  os.getenv('SECRET_KEY')
if not app.secret_key:
    raise ValueError("SECRET_KEY não configurada! Defina-a no arquivo .env ou como variável de ambiente.")

app.register_blueprint(rotas.auth.auth_bp)
app.register_blueprint(rotas.main.main_bp)
app.register_blueprint(rotas.api.api_bp, url_prefix='/api')

# Inicia o servidor Flask em modo debug
if __name__ == '__main__':
    app.run()










