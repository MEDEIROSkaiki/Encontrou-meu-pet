from utils.with_connection import with_connection

@with_connection
def get_racas_por_id_especie(cursor, idespecie):
    cursor.execute(
        "SELECT idRaca, nome, idespecie FROM RACA WHERE idespecie = ?", 
        (idespecie,)
    )
    return [{'id': row.idRaca, 'nome': row.nome} for row in cursor.fetchall()]
