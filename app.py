
# Importa as bibliotecas necessárias
# Flask é o microframework para web e pyodbc é usado para conectar ao SQL Server
from flask import Flask,jsonify, request, render_template
from db.racas_db import get_racas_por_id_especie
from db.especies_db import get_all_especies
from db.generos_db import get_all_generos
from db.portes_db import get_all_portes
from db.situacoes_db import get_all_situacoes
from db.usuario_db import email_existente, adicionar_usuario

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

@app.route('/cadastrar', methods=['POST'])
def adicionar_usuario_route():
    data = request.get_json()
    nome = data.get('nome', '').strip()
    email = data.get('email', '').strip()
    senha = data.get('senha', '')
    confirmar = data.get('confirmar', '')

    if senha != confirmar:
        return jsonify({'status': 'erro', 'mensagem': 'Senhas não conferem'})

    if email_existente(email):
        return jsonify({'status': 'erro', 'mensagem': 'E-mail já cadastrado'})

    adicionar_usuario(nome, email, senha)
    return jsonify({'status': 'sucesso', 'mensagem': 'Usuário cadastrado com sucesso!'})

    return render_template('cadastro_criado.html')

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

@app.route('/anunciar/cadastro2')
def anunciar_cadastro2():
    return render_template('cadastro/cadastro_2.html')

@app.route('/anunciar/get_all_especies')
def get_all_especies_route():
    try:
        especies = get_all_especies()
        return jsonify(especies)
    
    except Exception as e:
        return jsonify({'erro': str(e)}), 500  
    
@app.route('/anunciar/get_all_generos')
def get_all_generos_route():
    try:
        generos = get_all_generos()
        return jsonify(generos)
    
    except Exception as e:
        return jsonify({'erro': str(e)}), 500   

@app.route('/anunciar/get_all_portes')
def get_all_portes_route():
    try:
        portes = get_all_portes()
        return jsonify(portes)
    
    except Exception as e:
        return jsonify({'erro': str(e)}), 500     

@app.route('/anunciar/get_all_situacoes')
def get_all_situacoes_route():
    try:
        situacoes = get_all_situacoes()
        return jsonify(situacoes)
    
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






@app.route('/cadastrar_animal', methods=['POST'])
def cadastrar_animal():
    data = request.get_json()

    raca = data.get('raca', '').strip()
    porte = data.get('porte', '').strip()
    situacao = data.get('situacao', '').strip()
    genero = data.get('genero', '').strip()
    especie = data.get('especie', '').strip()

    # Validação simples
    if not all([raca, porte, situacao, genero, especie]):
        return jsonify({'erro': 'Todos os campos são obrigatórios.'}), 400

    # Aqui você pode adicionar lógica para salvar no banco, por exemplo
    # salvar_animal_no_banco(raca, porte, situacao, genero, especie)

    return jsonify({'mensagem': 'Animal cadastrado com sucesso!'}), 200




