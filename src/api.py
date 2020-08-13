import decimal
import json
import pymysql
from flask import Flask, request, abort, Response

from config_bd import conf
from sql_queries import *

app = Flask(__name__)
api_rota_produto = '/webservice/produto'
api_rota_estatisticas = '/webservice/stats'
conn = pymysql.connect(**conf)
cursor = conn.cursor()


def dec_serializer(o):
    if isinstance(o, decimal.Decimal):
        return float(o)


def validar_id_lancar_erro(produto_id: int):
    cursor.execute(sql_produto_find_by_id(produto_id))
    produto = json.dumps(cursor.fetchone(), default=dec_serializer)

    if not produto or produto == 'null':
        abort(Response('Produto não encontrado', 404))


def validar_produto_lancar_erro(**produto):
    chaves_obrigatorias = ['preco', 'quantidade', 'nome', 'descricao']

    # verifique se o produto não é nulo
    if not produto or produto == 'null':
        abort(Response('O produto de entrada não pode ser nulo', 400))

    # verifique se todas propriedades estão preenchidas
    nome_props_nulas = [c for c in chaves_obrigatorias
                        if c not in produto or not str(produto[c]).strip()]

    if nome_props_nulas:
        propriedades_texto = ', '.join(nome_props_nulas)
        abort(Response(f'É necessário preencher os campos: {propriedades_texto}', 400))

    # verifique se o preço ou a quantidade é negativa
    props_negativas = [prop for prop in ['preco', 'quantidade'] if produto[prop] < 0]

    if props_negativas:
        propriedades_texto = ', '.join(props_negativas)
        abort(Response(f'Os seguintes campos não podem ser negativos: {propriedades_texto}', 400))


@app.route(f'{api_rota_produto}/<int:id>', methods=['DELETE'])
def produto_delete(id: int):
    validar_id_lancar_erro(id)

    try:
        conn.begin()
        cursor.execute(sql_produto_delete_nome_desc(id))
        cursor.execute(sql_produto_delete_preco_qtd(id))
        conn.commit()
        return {}

    except Exception as e:
        conn.rollback()
        abort(Response(e.__doc__ + str(e), 500))


@app.route(api_rota_produto, methods=['GET'])
def produto_get():
    try:
        cursor.execute(sql_produto_find())
        return json.dumps(cursor.fetchall(), default=dec_serializer)

    except Exception as e:
        abort(Response(e.__doc__ + str(e), 500))


@app.route(f'{api_rota_produto}/<int:id>', methods=['GET'])
def produto_get_by_id(id: int):
    validar_id_lancar_erro(id)

    try:
        cursor.execute(sql_produto_find_by_id(id))
        return json.dumps(cursor.fetchone(), default=dec_serializer)

    except Exception as e:
        abort(Response(e.__doc__ + str(e), 500))


@app.route(f'{api_rota_produto}/<int:id>', methods=['PUT'])
def produto_put(id: int):
    # Valide o ID e a entrada
    entrada: dict = json.loads(request.data.decode('utf-8'))
    validar_id_lancar_erro(id)
    validar_produto_lancar_erro(**entrada)

    try:
        # Inicie uma transação com o banco
        conn.begin()

        # Monte e execute o SQL p/ criar um post c/ o nome e a descrição do produto
        sql_nome_desc = sql_produto_update_nome_desc(id, entrada['nome'], entrada['descricao'])
        cursor.execute(sql_nome_desc)
        prod_id = id

        # Monte e exec. o SQL p/ atualizar o preço
        sql_preco = sql_produto_update_preco(prod_id, entrada['preco'])
        cursor.execute(sql_preco)

        # Monte e exec. o SQL p/ atualizar a quantidade
        sql_qtd = sql_produto_update_qtd(prod_id, entrada['quantidade'])
        cursor.execute(sql_qtd)
        conn.commit()

        # Retorne o dado de entrada acrescido de seu ID
        return {**entrada, 'id': prod_id}

    # Em caso de erro, reverta todos updates
    except Exception as e:
        conn.rollback()
        abort(Response(e.__doc__ + str(e), 500))


@app.route(api_rota_produto, methods=['POST'])
def produto_post():
    entrada: dict = json.loads(request.data.decode('utf-8'))
    validar_produto_lancar_erro(**entrada)

    try:
        # Inicie uma transação com o banco
        conn.begin()

        # Monte e execute o SQL p/ criar um post c/ o nome e a descrição do produto
        sql1 = sql_produto_create_nome_desc(entrada['nome'], entrada['descricao'])
        cursor.execute(sql1)
        prod_id = conn.insert_id()

        # Monte e exec. o SQL p/ inserir o preço e quantidade em estoque
        sql2 = sql_produto_create_preco_qtd(prod_id, entrada['quantidade'], entrada['preco'])
        cursor.execute(sql2)
        conn.commit()

        # Retorne o dado de entrada acrescido de seu ID
        return {**entrada, 'id': prod_id}

    # Em caso de erro, reverta todos inserts
    except Exception as e:
        conn.rollback()
        abort(Response(e.__doc__ + str(e), 500))


@app.route(api_rota_estatisticas, methods=['GET'])
def estatisticas_get():
    try:
        cursor.execute(sql_estatisticas())
        return json.dumps(cursor.fetchone(), default=dec_serializer)

    except Exception as e:
        abort(Response(e.__doc__ + str(e), 500))


if __name__ == '__main__':
    app.run(debug=False)
