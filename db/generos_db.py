from utils.with_connection import with_connection

@with_connection
def get_all_generos(cursor):
    cursor.execute(
        "SELECT idGenero, nome FROM GENERO"
    )
    return [{'id': row.idGenero, 'nome': row.nome} for row in cursor.fetchall()]
