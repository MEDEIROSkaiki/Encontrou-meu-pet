from utils.with_connection import with_connection

@with_connection
def get_all_portes(cursor):
    cursor.execute(
        "SELECT idPorte, nome FROM PORTE"
    )
    return [{'id': row.idPorte, 'nome': row.nome} for row in cursor.fetchall()]
