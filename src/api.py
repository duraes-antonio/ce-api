import decimal, json, pymysql
from sql_queries import *
from flask import Flask, request


def dec_serializer(o):
    if isinstance(o, decimal.Decimal):
        return float(o)


app = Flask(__name__)
api_rota = '/webservice/produto'
db_nome = 'loja'
conf = {
    "host": "127.0.0.1",
    "port": 3306,
    "user": "root",
    "passwd": "",
    "charset": "utf8mb4",
    "cursorclass": pymysql.cursors.DictCursor,
    "database": db_nome
}
conn = pymysql.connect(**conf)
cursor = conn.cursor()

# TODO: Implementar
@app.route(f'{api_rota}/<int:id>', methods=['DELETE'])
def delete(id: int):

    try:
        # TODO: Tratar existência do produto
        cursor.execute(sql_produto_delete(id))
        conn.commit()
        return {}

    except Exception as e:
        raise e

# TODO: Implementar
@app.route(api_rota, methods=['GET'])
def get():
    cursor.execute(sql_produto_find())
    return json.dumps(cursor.fetchall(), default=dec_serializer)

# TODO: Implementar
@app.route(f'{api_rota}/<int:id>', methods=['GET'])
def get_by_id(id: int):
    cursor.execute(sql_produto_find_by_id(id))
    return json.dumps(cursor.fetchone(), default=dec_serializer)

# TODO: Implementar
@app.route(f'{api_rota}/<int:id>', methods=['PATCH'])
def patch(id: int):

    try:
        print()

    except:
        print()

    return

# TODO: Implementar
@app.route(api_rota, methods=['POST'])
def post():

    try:
        entrada = json.loads(request.data.decode('utf-8'))

        # Inicie uma transação com o banco
        conn.begin()

        # Monte e execute o SQL p/ criar um post c/ o nome e a descrição do produto
        sql1 = sql_produto_create_nome_desc(entrada['nome'], entrada['descricao'])
        cursor.execute(sql1)
        prod_id = conn.insert_id()

        # Monte e exec. o SQL p/ inserir o preço e quantidade em estoque
        sql2 = sql_produto_create_postmeta(prod_id, entrada['quantidade'], entrada['preco'])
        cursor.execute(sql2)
        conn.commit()

        # Retorne o dado de entrada acrescido de seu ID
        return {**entrada, 'id': prod_id}

    # Em caso de erro, reverta todos inserts
    except Exception as e:
        conn.rollback()
        raise e

if __name__ == '__main__':
    app.run(debug=False)
