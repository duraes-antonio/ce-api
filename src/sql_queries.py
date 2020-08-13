def sql_produto_find() -> str:
    return f"""
        SELECT
            ID AS id,
            post_title AS nome,
            post_content AS descricao,
            tb_preco.meta_value AS preco,
            tb_qtd.meta_value AS quantidade
        FROM wp_posts AS tb_post

            INNER JOIN
            (SELECT meta_value, post_id FROM wp_postmeta WHERE meta_key = '_price')
            AS tb_preco ON tb_preco.post_id = ID

            INNER JOIN
            (SELECT meta_value, post_id FROM wp_postmeta WHERE meta_key = '_stock')
            AS tb_qtd ON tb_qtd.post_id = ID
        WHERE post_type = 'product'
        """

def sql_produto_find_by_id(id: int) -> str:
    return f"""{sql_produto_find()} AND ID = {id}"""


def sql_produto_delete(id: int) -> str:
    return f"""
        DELETE FROM wp_wc_product_meta_lookup WHERE product_id = {id};
        """


def sql_produto_create_nome_desc(nome: str, descricao: str) -> str:
    return f"""
        INSERT INTO wp_posts (post_title, post_content, post_type)
        VALUES ('{nome}', '{descricao}', 'product');
        """

def sql_produto_create_preco_qtd(post_id: int, quantidade: int, preco: float) -> str:
    return f"""
        INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
        VALUES
            ({post_id}, '_price', {preco}),
            ({post_id}, '_stock', {quantidade}),
            ({post_id}, '_manage_stock', 'yes')
        ;
        """


def sql_produto_update_nome_desc(post_id: int, nome: str, descricao: str) -> str:
    return f"""
        UPDATE wp_posts
        SET
            post_title = '{nome}',
            post_content = '{descricao}'
        WHERE ID = {post_id};
        """

def sql_produto_update_qtd(post_id: int, quantidade: int) -> str:
    return f"""
        UPDATE wp_postmeta
        SET meta_value = {quantidade}
        WHERE post_id = {post_id} AND meta_key = '_stock';
        """

def sql_produto_update_preco(post_id: int, preco: float) -> str:
    return f"""
        UPDATE wp_postmeta
        SET meta_value = {preco}
        WHERE post_id = {post_id} AND meta_key = '_price';
        """
