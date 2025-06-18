from utils.with_connection import with_connection

@with_connection
def adicionar_pet(
    cursor,
    usuario_id,
    porte_id,
    situacao_id,
    raca_id,
    genero_id,
    nome_pet,
    municipio,
    estado,
    data_cadastro,
    cor,
    olhos,
    descricao,
    imagem_path
):
    try:
        # Comando INSERT para a tabela Usuario_Pet
        cursor.execute(
            """
            INSERT INTO Usuario_Pet (
                IdUsuario, IdPorte, IdSituacao, IdRaca, IdGenero, NomePet,
                Cidade, Estado, DataOcorrencia, CorPredominante, CorOlhos, Descricao, Imagem
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            usuario_id,
            porte_id,
            situacao_id,
            raca_id,
            genero_id,
            nome_pet,
            municipio,
            estado,
            data_cadastro,
            cor,
            olhos,
            descricao,
            imagem_path
        )
        return True
    except Exception as e:
        print(f"Erro ao inserir pet no DB: {e}")
        return False