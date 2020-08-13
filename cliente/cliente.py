import json
import inquirer
import requests


def formatar_saida_prod(**produto) -> str:
    resp_vazia = 'Não informado'

    def valor_ou_campo_nao_informado(valor: any) -> str:
        return str(valor) if valor else resp_vazia

    qtd_str = f"{int(float(produto['quantidade']))} unidades" if produto['quantidade'] else resp_vazia

    produto_str = f"""
    Id:\t\t\t{valor_ou_campo_nao_informado(produto['id'])}
    Nome:\t\t{valor_ou_campo_nao_informado(produto['nome'])}
    Descrição:\t\t{valor_ou_campo_nao_informado(produto['descricao'])}
    Preço:\t\tR${valor_ou_campo_nao_informado(produto['preco'])}
    Quantidade:\t\t{qtd_str}"""
    return produto_str

def formatar_erro(err: requests.Response) -> str:
    return f"#ERRO: {err.content.decode('utf8')}"


def listar_produtos(api_url_prod: str):
    r = requests.get(api_url_prod)
    [print(formatar_saida_prod(**p)) for p in r.json()]

def listar_produto(api_url_prod: str):
    id = int(input('\nDigite o id do produto buscado: '))
    resposta = requests.get(f"{api_url_prod}/{id}")
    saida = formatar_saida_prod(**resposta.json()) if resposta.ok else formatar_erro(resposta)
    print(saida)

def registrar_produto(api_url_prod: str):
    nome = input('\nDigite o NOME do produto: ')
    desc = input('\nDigite a DESCRIÇÃO do produto: ')
    preco = float(input('\nDigite o PREÇO do produto (Ex: 12.76): '))
    qtd = int(input('\nDigite a QUATIDADE do produto (número inteiro): '))
    entrada = {'nome': nome, 'descricao': desc, 'quantidade': qtd, 'preco': preco}
    resposta = requests.post(api_url_prod, data=json.dumps(entrada))
    saida = formatar_saida_prod(**resposta.json()) if resposta.ok else formatar_erro(resposta)
    print(saida)

def atualizar_produto(api_url_prod: str):
    id = int(input('\nDigite o ID do produto a ser atualizado: '))
    nome = input('\nDigite o novo NOME do produto: ')
    desc = input('\nDigite a nova DESCRIÇÃO do produto: ')
    preco = float(input('\nDigite o novo PREÇO do produto (Ex: 12.76): '))
    qtd = int(input('\nDigite a nova QUATIDADE do produto (número inteiro): '))

    entrada = {'nome': nome, 'descricao': desc, 'quantidade': qtd, 'preco': preco}
    resposta = requests.put(f"{api_url_prod}/{id}", data=json.dumps(entrada))
    saida = formatar_saida_prod(**resposta.json()) if resposta.ok else formatar_erro(resposta)
    print(saida)

def remover_produto(api_url_prod: str):
    id = int(input('\nDigite o id do produto a ser REMOVIDO: '))
    resposta = requests.delete(f"{api_url_prod}/{id}")
    saida = '#INFO: Produto removido com sucesso!' if resposta.ok else formatar_erro(resposta)
    print(f"{saida}\n")

def obter_estatisticas(api_url_estatisticas: str):

    def formatar_estats(resposta: requests.Response) -> str:
        resp_json = resposta.json()
        qtd_vendida = f"Unidades vendidas:\t%d" %int(float(resp_json['qtd_total_produtos']))
        valor_vendido = f"Valor total:\t\tR$%.2f" %float(resp_json['valor_total_produtos'])
        valor_medio = f"Valor médio (produto):\tR$%.2f" %float(resp_json['valor_medio_produtos'])
        return f"""{qtd_vendida}\n{valor_vendido}\n{valor_medio}"""

    resposta = requests.get(api_url_estatisticas)
    saida = formatar_estats(resposta) if resposta.ok else formatar_erro(resposta)
    print(saida)

def main():
    op_sair = 'Sair'
    msg_sair = '\nSaindo...'
    menu_titulo = 'Qual operação deseja realizar com a API?'
    menu_opcoes = [
        'Listar produtos', 'Listar produto', 'Inserir produto',
        'Atualizar produto', 'Remover produto', 'Obter estatísticas', op_sair
    ]
    menu = [inquirer.List('op', message=menu_titulo, choices=menu_opcoes)]

    api_url = 'http://localhost:5000/webservice'
    api_produto = f'{api_url}/produto'
    api_estatisticas = f'{api_url}/stats'

    try:
        resposta: dict = inquirer.prompt(menu)

        while (resposta and resposta['op'] != op_sair):
            op = resposta['op']

            if (op == 'Listar produtos'):
                listar_produtos(api_produto)

            elif (op == 'Listar produto'):
                listar_produto(api_produto)

            elif (op == 'Inserir produto'):
                registrar_produto(api_produto)

            elif (op == 'Atualizar produto'):
                atualizar_produto(api_produto)

            elif (op == 'Remover produto'):
                remover_produto(api_produto)

            elif (op == 'Obter estatísticas'):
                obter_estatisticas(api_estatisticas)

            print()
            resposta: dict = inquirer.prompt(menu)
        print(msg_sair)

    except KeyboardInterrupt:
        print(msg_sair)


if __name__ == "__main__":
    main()
