from flask import Blueprint, render_template, flash, redirect, get_flashed_messages,url_for, jsonify, session, request

import bcrypt

import db.dicionarios_db as db_dic
import db.usuario_db as db_user

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/login')
def login():
    return render_template('login.html')

@auth_bp.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    senha = request.form.get('senha')
    if not email or not senha:
        flash('E-mail e senha são obrigatórios.', 'error')
        return redirect(url_for("auth_bp.login"))

    # 1. Buscar o usuário pelo e-mail
    usuario = db_user.buscar_usuario_por_email(email)

    if not usuario:
        flash('Credenciais inválidas.', 'error')
        return redirect(url_for("auth_bp.login"))

    try:
        if bcrypt.checkpw(senha.encode('utf-8'), usuario['hashed_senha'].encode('utf-8')):
            session['esta_logado'] = True
            session['usuario_id'] = usuario['id']
            session['usuario_email'] = usuario['email']
            session['usuario_name'] = usuario['nome']

            return redirect(url_for("main_bp.index"))
        else:
            flash('Credenciais inválidas.', 'error')
            return redirect(url_for("auth_bp.login"))
    except ValueError:
        flash('Houve um erro, tente mais tarde.', 'error')
        return redirect(url_for("auth_bp.login"))


@auth_bp.route('/cadastrar')
def cadastrar():
    return render_template('cadastro_usuario.html',form_data={})

@auth_bp.route('/cadastrar', methods=['POST'])
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

    if db_user.email_existente(email):
        flash( 'E-mail já cadastrado', 'error')
        return render_template('cadastro_usuario.html', messages=get_flashed_messages(with_categories=True), form_data=data.to_dict())

    try:
        db_user.adicionar_usuario(nome, sobrenome, email, hashed_senha, ddd, telefone, endereco_completo,complemento,bairro, cidade, estado)
        usuario = db_user.buscar_usuario_por_email(email)
        
        session['esta_logado'] = True
        session['usuario_id'] = usuario['id']
        session['usuario_email'] = usuario['email']
        session['usuario_name'] = usuario['nome']
        return redirect(url_for("main_bp.index"))          
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
        return redirect(url_for("main_bp.index"))     

@auth_bp.route('/logout')
def logout():
    session.pop('esta_logado',None)
    session.pop('usuario_id',None)
    session.pop('usuario_email',None)
    session.pop('usuario_name',None)
    return render_template('index.html')