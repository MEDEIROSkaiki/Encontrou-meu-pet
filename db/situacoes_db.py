from utils.with_connection import with_connection

@with_connection
def get_all_situacoes(cursor):
    cursor.execute(
        "SELECT idSituacao, nome FROM SITUACAO"
    )
    return [{'id': row.idSituacao, 'nome': row.nome} for row in cursor.fetchall()]
