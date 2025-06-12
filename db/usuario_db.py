from utils.with_connection import with_connection

@with_connection
def email_existente(cursor,email):
    cursor.execute(
        "SELECT TOP 1 IdUsuario, Nome, Email FROM USUARIO WHERE Email = ?",(email)
    )
    return [{'id': row.IdUsuario, 'nome': row.nome, 'email': row.Email} for row in cursor.fetchall()]

@with_connection
def adicionar_usuario(cursor, nome, email, senha):
    cursor.execute(
                """INSERT INTO USUARIO (Nome, Sobrenome, Email, DDD, Telefone, Endereco, Bairro, Cidade, Estado)
                    VALUES (?, NULL, ?, NULL, NULL, NULL, NULL, NULL,NULL)""",
        (nome, email)
    )
