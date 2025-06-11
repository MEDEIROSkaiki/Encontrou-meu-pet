
# Importa as bibliotecas necessárias
# Flask é o microframework para web e pyodbc é usado para conectar ao SQL Server
from flask import Flask,jsonify, request, render_template
from db.racas_db import get_racas_por_id_especie
from db.especies_db import get_all_especies

# Cria uma instância da aplicação Flask
app = Flask(__name__)

# Rota principal: exibe o formulário HTML (form.html deve estar na pasta 'templates')
@app.route('/')
def index():
    return render_template('index.html')  # Mostra a página com o formulário de entrada

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/cadastrar')
def cadastrar():
    return render_template('cadastro_usuario.html')

@app.route('/pesquisa')
def pesquisa():
    return render_template('pesquisa.html')

# Rota para tratar os dados enviados pelo formulário (método POST)
@app.route('/enviar', methods=['POST'])
def enviar():
    pass

@app.route('/anunciar/cadastro')
def anunciar_cadastro():
    return render_template('cadastro/cadastro.html')

@app.route('/anunciar/get_all_especies')
def get_all_especies_route():
    try:
        especies = get_all_especies()
        return jsonify(especies)
    
    except Exception as e:
        return jsonify({'erro': str(e)}), 500  

@app.route('/racas', methods=['POST'])    
def get_racas_por_id_especie_route():
    try:
        data = request.get_json()  # pega os dados JSON enviados pelo front
        idespecie = data.get('idespecie')  # pega o idespecie do JSON
        
        if idespecie is None:
            return jsonify({'erro': 'idespecie é obrigatório'}), 400
        
        racas = get_racas_por_id_especie(idespecie)
        return jsonify(racas)
    
    except Exception as e:
        return jsonify({'erro': str(e)}), 500  

# Inicia o servidor Flask em modo debug
if __name__ == '__main__':
    app.run(debug=True)

