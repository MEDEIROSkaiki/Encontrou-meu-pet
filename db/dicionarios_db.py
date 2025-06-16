from utils.with_connection import with_connection

@with_connection
def get_all_especies(cursor):
    cursor.execute(
      "SELECT idEspecie, nome FROM ESPECIE"
    )
    return [{'idEspecie': row.idEspecie, 'nome': row.nome} for row in cursor.fetchall()]

@with_connection
def get_all_generos(cursor):
    cursor.execute(
        "SELECT idGenero, nome FROM GENERO"
    )
    return [{'id': row.idGenero, 'nome': row.nome} for row in cursor.fetchall()]

@with_connection
def get_all_portes(cursor):
    cursor.execute(
        "SELECT idPorte, nome FROM PORTE"
    )
    return [{'id': row.idPorte, 'nome': row.nome} for row in cursor.fetchall()]

@with_connection
def get_racas_por_id_especie(cursor, idespecie):
    cursor.execute(
        "SELECT idRaca, nome, idespecie FROM RACA WHERE idespecie = ?", 
        (idespecie,)
    )
    return [{'id': row.idRaca, 'nome': row.nome} for row in cursor.fetchall()]


@with_connection
def get_all_situacoes(cursor):
    cursor.execute(
        "SELECT idSituacao, nome FROM SITUACAO"
    )
    return [{'id': row.idSituacao, 'nome': row.nome} for row in cursor.fetchall()]

