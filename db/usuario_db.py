from utils.with_connection import with_connection

@with_connection
def email_existente(cursor,email):
    cursor.execute(
        "SELECT TOP 1 IdUsuario, Nome, Email FROM USUARIO WHERE Email = ?",(email)
    )
    return [{'id': row.IdUsuario, 'nome': row.Nome, 'email': row.Email} for row in cursor.fetchall()]

@with_connection
def adicionar_usuario(cursor, nome, sobrenome, email, senha, ddd, telefone, endereco_completo, complemento,bairro, cidade, estado ):
    cursor.execute(
                """INSERT INTO USUARIO (Nome, Sobrenome, Email, DDD, Telefone, Endereco, Bairro, Cidade, Estado,Senha,Complemento)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?,?,?,?)""",
        (nome, sobrenome, email, ddd,telefone,endereco_completo,bairro,cidade,estado,senha,complemento)
    )

@with_connection
def buscar_usuario_por_email(cursor,email):
    cursor.execute("SELECT IdUsuario, Email, Senha, Nome, Sobrenome FROM Usuario WHERE Email = ?", email)
    usuario = cursor.fetchone() # Retorna a primeira linha encontrada
    if usuario:     
        return {
            'id': usuario[0],
            'email': usuario[1],
            'hashed_senha': usuario[2],
            'nome': usuario[3],
            'sobrenome': usuario[4]
        }
    return None