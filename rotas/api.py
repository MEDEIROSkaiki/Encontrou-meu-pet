
from flask import Blueprint, jsonify, request

import db.dicionarios_db as db_dic


api_bp = Blueprint('api_bp', __name__)

@api_bp.route('/anunciar/get_all_especies')
def get_all_especies_route():
    try:
        especies = db_dic.get_all_especies()
        return jsonify(especies)
    
    except Exception as e:
        return jsonify({'erro': str(e)}), 500  
    
@api_bp.route('/anunciar/get_all_generos')
def get_all_generos_route():
    try:
        generos = db_dic.get_all_generos()
        return jsonify(generos)
    
    except Exception as e:
        return jsonify({'erro': str(e)}), 500   

@api_bp.route('/anunciar/get_all_portes')
def get_all_portes_route():
    try:
        portes = db_dic.get_all_portes()
        return jsonify(portes)
    
    except Exception as e:
        return jsonify({'erro': str(e)}), 500     

@api_bp.route('/anunciar/get_all_situacoes')
def get_all_situacoes_route():
    try:
        situacoes = db_dic.get_all_situacoes()
        return jsonify(situacoes)
    
    except Exception as e:
        return jsonify({'erro': str(e)}), 500           

@api_bp.route('/racas', methods=['POST'])    
def get_racas_por_id_especie_route():
    try:
        data = request.get_json()  # pega os dados JSON enviados pelo front
        idespecie = data.get('idespecie')  # pega o idespecie do JSON
        
        if idespecie is None:
            return jsonify({'erro': 'idespecie é obrigatório'}), 400
        
        racas = db_dic.get_racas_por_id_especie(idespecie)
        return jsonify(racas)
    
    except Exception as e:
        return jsonify({'erro': str(e)}), 500  