
# Importa as bibliotecas necessárias
# Flask é o microframework para web e pyodbc é usado para conectar ao SQL Server
from flask import Flask,jsonify, request, render_template
import pyodbc

# Cria uma instância da aplicação Flask
app = Flask(__name__)

# Define a string de conexão com o SQL Server
# - DRIVER: nome do driver ODBC instalado (verificado com `pyodbc.drivers()`)
# - SERVER: nome do servidor (localhost se estiver local)
# - DATABASE: nome do banco de dados
# - UID e PWD: usuário e senha criados no SQL Server
conn_str = (
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=localhost\\ProjetoSenai;'  # ou o nome do servidor SQL, como 'SENAI103\SQLEXPRESS'
    'DATABASE=MEU-PET-DB;'  # nome do banco criado no SQL Server
    'UID=user_projeto;'    # usuário com permissões no banco
    'PWD=senai103@' # senha definida ao criar o usuário
)

# Rota principal: exibe o formulário HTML (form.html deve estar na pasta 'templates')
@app.route('/')
def index():
    return render_template('cadastro_2.html')  # Mostra a página com o formulário de entrada

# Rota para tratar os dados enviados pelo formulário (método POST)
@app.route('/enviar', methods=['POST'])
def enviar():
    # Captura os dados do formulário HTML enviados pelo usuário
    nome = request.form['nome']
    email = request.form['email']

    try:
        # Abre a conexão com o banco usando a string de conexão definida
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        # Executa o comando SQL para inserir os dados na tabela Contatos
        # Os "?" são usados como parâmetros para prevenir SQL Injection
        cursor.execute("INSERT INTO RACA (nome, idespecie) VALUES (?, ?)", ("Poodle", 1))

        # Salva as mudanças no banco de dados
        conn.commit()

        # Fecha o cursor e a conexão
        cursor.close()
        conn.close()

        # Mensagem de sucesso com link para voltar ao formulário
        return f"<h2>Dados salvos com sucesso!</h2><a href='/'>Voltar</a>"

    except Exception as e:
        # Em caso de erro, exibe o erro no navegador
        return f"<h2>Erro ao salvar no banco:</h2><pre>{e}</pre>"

@app.route('/racas')    
def racas():
    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        cursor.execute("SELECT idRaca, nome, idespecie FROM RACA")
        racas = [{'id': row.idRaca, 'nome': row.nome, 'idespecie': row.idespecie} for row in cursor.fetchall()]

        cursor.close()
        conn.close()

        return jsonify(racas)
    
    except Exception as e:
        return jsonify({'erro': str(e)})    

# Inicia o servidor Flask em modo debug
if __name__ == '__main__':
    app.run(debug=True)

