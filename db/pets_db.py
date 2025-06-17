from utils.with_connection import with_connection

@with_connection
def adicionar_pet(cursor,email):
    cursor.execute(
        "SELECT TOP 1 IdUsuario, Nome, Email FROM USUARIO WHERE Email = ?",(email)
    )
    return [{'id': row.IdUsuario, 'nome': row.Nome, 'email': row.Email} for row in cursor.fetchall()]