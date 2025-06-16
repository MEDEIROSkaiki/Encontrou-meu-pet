
# Importa as bibliotecas necessárias
# Flask é o microframework para web e pyodbc é usado para conectar ao SQL Server
from flask import Flask,jsonify, request, redirect, url_for,flash,get_flashed_messages, render_template,session 
import os
import bcrypt
from db import get_connection
from db.racas_db import get_racas_por_id_especie
from db.especies_db import get_all_especies
from db.generos_db import get_all_generos
from db.portes_db import get_all_portes
from db.situacoes_db import get_all_situacoes
from db.usuario_db import email_existente, adicionar_usuario,buscar_usuario_por_email



# Cria uma instância da aplicação Flask
app = Flask(__name__)


# Configure a SECRET_KEY a partir da variável de ambiente
app.secret_key =  os.getenv('SECRET_KEY')
if not app.secret_key:
    raise ValueError("SECRET_KEY não configurada! Defina-a no arquivo .env ou como variável de ambiente.")


# Rota principal: exibe o formulário HTML (form.html deve estar na pasta 'templates')
@app.route('/')
def index():
    return render_template('index.html')  # Mostra a página com o formulário de entrada

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    senha = request.form.get('senha')
    if not email or not senha:
        flash('E-mail e senha são obrigatórios.', 'error')
        return redirect(url_for("login"))

    # 1. Buscar o usuário pelo e-mail
    usuario = buscar_usuario_por_email(email)

    if not usuario:
        flash('Credenciais inválidas.', 'error')
        return redirect(url_for("login"))

    try:
        if bcrypt.checkpw(senha.encode('utf-8'), usuario['hashed_senha'].encode('utf-8')):
            session['esta_logado'] = True
            session['usuario_id'] = usuario['id']
            session['usuario_email'] = usuario['email']
            session['usuario_name'] = usuario['nome']

            return redirect(url_for("index"))
        else:
            flash('Credenciais inválidas.', 'error')
            return redirect(url_for("login"))
    except ValueError:
        flash('Houve um erro, tente mais tarde.', 'error')
        return redirect(url_for("login"))


@app.route('/cadastrar')
def cadastrar():
    return render_template('cadastro_usuario.html',form_data={})

@app.route('/cadastrar', methods=['POST'])
def adicionar_usuario_route():
    data = request.form
    nome = data.get('nome', '').strip()
    sobrenome = data.get('sobrenome', '')
    email = data.get('email', '').strip()
    senha = data.get('senha', '')
    confirmar = data.get('confirmar', '')
    ddd = data.get('ddd', '')
    telefone = data.get('telefone', '')
    endereco = data.get('endereco', '')
    numero = data.get('numero', '')
    complemento = data.get('complemento', '')
    bairro = data.get('bairro', '')
    cidade = data.get('cidade', '')
    estado = data.get('estado', '')

    endereco_completo = endereco 
    if numero:
        endereco_completo += ", " + numero

    if not all([nome, sobrenome, email, senha, confirmar, endereco, bairro, cidade, estado]):
        flash('Por favor, preencha todos os campos obrigatórios.', 'error')
        return render_template('cadastro_usuario.html', messages=get_flashed_messages(with_categories=True), form_data=data.to_dict())

    hashed_senha = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    if senha != confirmar:
        flash('Senhas não conferem', 'error')
        return render_template('cadastro_usuario.html', messages=get_flashed_messages(with_categories=True), form_data=data.to_dict())

    if email_existente(email):
        flash( 'E-mail já cadastrado', 'error')
        return render_template('cadastro_usuario.html', messages=get_flashed_messages(with_categories=True), form_data=data.to_dict())

    try:
        adicionar_usuario(nome, sobrenome, email, hashed_senha, ddd, telefone, endereco_completo,complemento,bairro, cidade, estado)
        usuario = buscar_usuario_por_email(email)
        
        session['esta_logado'] = True
        session['usuario_id'] = usuario['id']
        session['usuario_email'] = usuario['email']
        session['usuario_name'] = usuario['nome']
        return redirect(url_for("index"))          
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
        return redirect(url_for("index"))     

@app.route('/logout')
def logout():
    session.pop('esta_logado',None)
    session.pop('usuario_id',None)
    session.pop('usuario_email',None)
    session.pop('usuario_name',None)
    return render_template('index.html')

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


# Inicia o servidor Flask em modo debug
if __name__ == '__main__':
    app.run()










