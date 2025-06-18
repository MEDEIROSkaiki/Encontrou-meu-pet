from flask import Blueprint, render_template, jsonify, session, request,flash,get_flashed_messages,redirect,url_for
from werkzeug.utils import secure_filename
import os
import uuid

from utils.login_verification import login_requerido
from db import dicionarios_db as db_dic, pets_db


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
    situacao_id = data.get('situacao', '').strip()
    
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
        'situacao_id':situacao_id
    }

    return redirect(url_for('main_bp.anunciar_cadastro2')) 


@main_bp.route('/anunciar/cadastro2')
@login_requerido
def anunciar_cadastro2():
    etapa1_data = session.get('cadastro_pet_etapa1_data')
    if not etapa1_data:
        flash('Por favor, complete a Etapa 1 do cadastro primeiro.', 'warning')
        return redirect(url_for('main_bp.anunciar_cadastro'))
    
    especie_id = etapa1_data.get('especie_id')

    if not especie_id:
        flash('Erro: ID da espécie não encontrado na Etapa 1. Por favor, reinicie o cadastro.', 'error')
        session.pop('cadastro_pet_step1_data', None)
        return redirect(url_for('main_bp.anunciar_cadastro'))
    
    racas = db_dic.get_racas_por_id_especie(especie_id)
    portes = db_dic.get_all_portes()

    return render_template('cadastro/cadastro_2.html', 
                           racas=racas,
                           portes = portes, 
                           form_data={},
                           messages=get_flashed_messages(with_categories=True))    


@main_bp.route('/anunciar/cadastro2', methods=['POST'])
@login_requerido
def anunciar_cadastro2_post():
    etapa1_data = session.get('cadastro_pet_etapa1_data')

    if not etapa1_data:
        flash('Por favor, complete a Etapa 1 do cadastro primeiro.', 'warning')
        return redirect(url_for('main_bp.anunciar_cadastro'))
    
    data = request.form
    
    raca_id = data.get('raca', '').strip()
    cor = data.get('cor', '').strip()
    olhos = data.get('olhos', '').strip() 
    porte = data.get('porte', '').strip() 
    dataOcorrencia = data.get('data', '').strip() 
    estado = data.get('estado', '').strip() 
    municipio = data.get('municipio', '').strip() 
    
    form_data = data.to_dict() 
    
    especie_id_etapa1 = etapa1_data.get('especie_id')
    racas_para_template = db_dic.get_racas_por_id_especie(especie_id_etapa1)

    campos_obrigatorios_etapa2 = [
        raca_id,
        cor,
        olhos,
        porte,
        dataOcorrencia,
        estado,
        municipio
    ]

    if not all(campos_obrigatorios_etapa2):
        flash('Por favor, preencha todos os campos obrigatórios da Etapa 2.', 'error')
        return render_template('cadastro/cadastro_2.html',
                               racas=racas_para_template,
                               etapa1_data=etapa1_data,
                               form_data=form_data,
                               messages=get_flashed_messages(with_categories=True))

    try:
        raca_id_int = int(raca_id)
    except ValueError:
        flash('O valor selecionado para Raça é inválido.', 'error')
        return render_template('cadastro/cadastro_2.html',
                               racas=racas_para_template,
                               etapa1_data=etapa1_data,
                               form_data=form_data,
                               messages=get_flashed_messages(with_categories=True))

    valid_racas_ids = [r['id'] for r in racas_para_template]
    if raca_id_int not in valid_racas_ids:
        flash('Raça selecionada é inválida ou não existe para esta espécie.', 'error')
        return render_template('cadastro/cadastro_2.html',
                               racas=racas_para_template,
                               etapa1_data=etapa1_data,
                               form_data=form_data,
                               messages=get_flashed_messages(with_categories=True))


    session['cadastro_pet_etapa2_data'] = {
        'raca_id': raca_id_int,
        'cor': cor,
        'olhos': olhos,
        "porte_id":porte,
        "dataOcorrencia":dataOcorrencia,
        "estado":estado,
        "municipio":municipio
    }

    return redirect(url_for('main_bp.anunciar_cadastro3'))

@main_bp.route('/anunciar/cadastro3')
@login_requerido
def anunciar_cadastro3():
    return render_template('cadastro/cadastro_3.html',form_data = {})


@main_bp.route('/anunciar/cadastro3', methods=['POST'])
@login_requerido
def anunciar_cadastro3_post():

    etapa1_data = session.get('cadastro_pet_etapa1_data')
    etapa2_data = session.get('cadastro_pet_etapa2_data')
    user_id = session.get('usuario_id')

    if not etapa1_data or not etapa2_data or not user_id:
        flash('Sessão de cadastro inválida ou usuário não logado. Por favor, reinicie o processo.', 'error')

        session.pop('cadastro_pet_etapa1_data', None)
        session.pop('cadastro_pet_etapa2_data', None)
        return redirect(url_for('main_bp.anunciar_cadastro'))


    descricao = request.form.get('descricao', '').strip()
    imagem_file = request.files.get('imagem')

    form_data_current_step = {'descricao': descricao}

    if not imagem_file:
        flash('Por favor, selecione uma imagem para o pet.', 'error')
        return render_template('cadastro/cadastro_3.html', 
                               form_data=form_data_current_step,
                               messages=get_flashed_messages(with_categories=True))

    if imagem_file.filename == '':
        flash('Nenhum arquivo de imagem selecionado.', 'error')
        return render_template('cadastro/cadastro_3.html', 
                               form_data=form_data_current_step,
                               messages=get_flashed_messages(with_categories=True))

    allowed_extensions = ['png', 'jpg', 'jpeg'] 

    if not allowed_file(imagem_file.filename, allowed_extensions):
        flash('Formato de imagem inválido. Apenas PNG, JPG e JPEG são permitidos.', 'error')
        return render_template('cadastro/cadastro_3.html', 
                                form_data=form_data_current_step,
                                messages=get_flashed_messages(with_categories=True))

    try:
        filename = secure_filename(imagem_file.filename)
        file_ext = os.path.splitext(filename)[1]
        

        new_filename = f"{user_id}_{uuid.uuid4()}{file_ext}"
        
        UPLOAD_FOLDER = os.path.join(os.getcwd(), 'static', 'pet_images') 
        
        os.makedirs(UPLOAD_FOLDER, exist_ok=True) 
        save_path = os.path.join(UPLOAD_FOLDER, new_filename)
        
        imagem_file.save(save_path)

        imagem_db_path = os.path.join('static', 'pet_images', new_filename) 
        
    except Exception as e:
        print(f"Erro ao salvar a imagem: {e}")
        flash('Ocorreu um erro ao salvar a imagem. Tente novamente.', 'error')
        return render_template('cadastro/cadastro_3.html', 
                               form_data=form_data_current_step,
                               messages=get_flashed_messages(with_categories=True))

    try:
        final_pet_data = {
            **etapa1_data,
            **etapa2_data,
            'descricao': descricao,
            'imagem_path': imagem_db_path,
            'usuario_id': user_id,
        }
        

        pets_db.adicionar_pet(
            usuario_id=final_pet_data['usuario_id'],
            porte_id=final_pet_data['porte_id'],
            situacao_id=final_pet_data['situacao_id'],
            raca_id=final_pet_data['raca_id'],
            genero_id=final_pet_data['genero_id'],
            nome_pet=final_pet_data['nome_pet'],
            municipio=final_pet_data['municipio'],
            estado=final_pet_data['estado'],
            data_cadastro=final_pet_data['dataOcorrencia'],
            cor=final_pet_data['cor'],
            olhos=final_pet_data['olhos'],
            descricao=final_pet_data['descricao'],
            imagem_path=final_pet_data['imagem_path']
        )
        

    except Exception as e:
        print(f"Erro ao salvar pet no banco de dados: {e}")
        flash('Ocorreu um erro ao finalizar o cadastro do pet. Tente novamente.', 'error')
        return render_template('cadastro/cadastro_3.html', 
                               form_data=form_data_current_step,
                               messages=get_flashed_messages(with_categories=True))

    session.pop('cadastro_pet_step1_data', None)
    session.pop('cadastro_pet_step2_data', None)

    flash('Pet cadastrado com sucesso!', 'success')
    return redirect(url_for('main_bp.index'))



def allowed_file(filename, allowed_extensions):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions
    

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