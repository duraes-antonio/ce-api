def sql_produto_find() -> str:
    return f"""
        SELECT
            product_id AS id,
            post_title AS nome,
            post_content AS descricao,
            stock_quantity AS quantidade,
            max_price AS preco
        FROM wp_wc_product_meta_lookup AS tb_produto
            INNER JOIN wp_posts AS tb_post
                ON tb_post.ID = tb_produto.product_id
        """

def sql_produto_find_by_id(id: int) -> str:
    return f"""
        SELECT
            product_id AS id,
            post_title AS nome,
            post_content AS descricao,
            stock_quantity AS quantidade,
            max_price AS preco
        FROM wp_wc_product_meta_lookup AS tb_produto
            INNER JOIN wp_posts AS tb_post
                ON tb_post.ID = tb_produto.product_id
        WHERE product_id = {id}
        """


def sql_produto_delete(id: int) -> str:
    return f"""
        DELETE FROM wp_wc_product_meta_lookup WHERE product_id = {id};
        """


def sql_produto_create_nome_desc(nome: str, descricao: str) -> str:
    return f"""
        INSERT INTO wp_posts (post_title, post_content, post_type)
        VALUES ('{nome}', '{descricao}', 'product');
        """

def sql_produto_create_qtd_preco(post_id: int, quantidade: int, preco: float) -> str:
    return f"""
        INSERT INTO wp_wc_product_meta_lookup (product_id, stock_quantity, min_price, max_price)
        VALUES ({post_id}, {quantidade}, {preco}, {preco});
        """

def sql_produto_create_postmeta(post_id: int, quantidade: int, preco: float) -> str:
    return f"""
        INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
        VALUES
            ({post_id}, '_price', {preco}),
            ({post_id}, '_stock', {quantidade}),
            ({post_id}, '_manage_stock', 'yes')
        ;
        """


def sql_produto_update_nome_desc(database: str, nome: str, descricao: str, id: int) -> str:
    return f"""
        USE {database};
        UPDATE wp_posts
        SET
            post_title = {nome},
            post_content = {descricao}
        WHERE ID = {id};
        """

def sql_produto_update_qtd_preco(database: str, quantidade: int, preco: float, id: int) -> str:
    return f"""
        USE {database};
        UPDATE wp_wc_product_meta_lookup
        SET
            stock_quantity = {quantidade},
            max_price = {preco}
        WHERE product_id = {id};
        """