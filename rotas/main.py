from flask import Blueprint, render_template, jsonify, session, request,flash,get_flashed_messages,redirect,url_for

from utils.login_verification import login_requerido
from db import dicionarios_db as db_dic


main_bp = Blueprint('main_bp', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/anunciar/pesquisa')
def pesquisa():
    return render_template('pesquisa.html')

@main_bp.route('/anunciar/cadastro')
@login_requerido
def anunciar_cadastro():    

    session.pop('cadastro_pet_etapa1_data',None)
    session.pop('nome_pet',None)
    session.pop('especie_id',None)
    session.pop('genero_id',None)

    especies = db_dic.get_all_especies()
    generos = db_dic.get_all_generos()

    return render_template('cadastro/cadastro.html', 
                           especies= especies, 
                           generos= generos, 
                           form_data={},
                           messages=get_flashed_messages(with_categories=True))

@main_bp.route('/anunciar/cadastro', methods=['POST'] )
@login_requerido
def anunciar_cadastro_post():
    
    data = request.form
        
    nome_pet = data.get('nome_pet', '').strip()
    especie_id = data.get('especie', '').strip()
    genero_id = data.get('genero', '').strip()
    
    form_data = request.form.to_dict()
    
    campos_obrigatorios = [
        nome_pet,
        especie_id,
        genero_id,
    ]

    if not all(campos_obrigatorios):
        flash('Por favor, preencha todos os campos obrigatórios.', 'error')
        # Recarrega as listas para os dropdowns
        especies = db_dic.get_all_especies()
        generos = db_dic.get_all_generos()
        return render_template('cadastro/cadastro.html', 
                               form_data=form_data, 
                               especies=especies, 
                               generos=generos,
                               messages=get_flashed_messages(with_categories=True))

    valid_especies = db_dic.get_all_especies()
    especie_id_int = int(especie_id)
    valid_especie_ids = [e['idEspecie'] for e in valid_especies]
    if especie_id_int not in valid_especie_ids:
        flash('Espécie inválida selecionada.', 'error')
        especies = db_dic.get_all_especies()
        generos = db_dic.get_all_generos()
        return render_template('cadastro/cadastro.html', 
                               form_data=form_data, 
                               especies=especies, 
                               generos=generos,
                               messages=flash.get_flashed_messages(with_categories=True))

    valid_generos = db_dic.get_all_generos()
    genero_id_int = int(genero_id)
    valid_genero_ids = [g['id'] for g in valid_generos]
    if genero_id_int not in valid_genero_ids:
        flash('Gênero inválido selecionado.', 'error')
        especies = db_dic.get_all_especies()
        generos = db_dic.get_all_generos()
        return render_template('cadastro/cadastro.html', 
                               form_data=form_data, 
                               especies=especies, 
                               generos=generos,
                               messages=get_flashed_messages(with_categories=True))

    session['cadastro_pet_etapa1_data'] = {
        'nome_pet': nome_pet,
        'especie_id': especie_id,
        'genero_id': genero_id,
    }

    return redirect(url_for('main_bp.anunciar_cadastro2')) 


@main_bp.route('/anunciar/cadastro2')
@login_requerido
def anunciar_cadastro2():
    return render_template('cadastro/cadastro_2.html')

@main_bp.route('/anunciar/cadastrar_animal', methods=['POST'])
@login_requerido
def cadastrar_animal():
    data = request.get_json()

    raca = data.get('raca', '').strip()
    porte = data.get('porte', '').strip()
    situacao = data.get('situacao', '').strip()
    genero = data.get('genero', '').strip()
    especie = data.get('especie', '').strip()

    if not all([raca, porte, situacao, genero, especie]):
        return jsonify({'erro': 'Todos os campos são obrigatórios.'}), 400

    return jsonify({'mensagem': 'Animal cadastrado com sucesso!'}), 200