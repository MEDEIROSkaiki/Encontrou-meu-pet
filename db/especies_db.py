from utils.with_connection import with_connection

@with_connection
def get_all_especies(cursor):
    cursor.execute(
      "SELECT idEspecie, nome FROM ESPECIE"
    )
    return [{'idEspecie': row.idEspecie, 'nome': row.nome} for row in cursor.fetchall()]
