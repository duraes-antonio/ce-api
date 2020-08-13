import inquirer
import requests




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
        resposta = inquirer.prompt(menu)

        while (resposta and resposta['op'] != op_sair):
            op = resposta['op']

            if (op == 'Listar produtos'):
                r = requests.get(api_produto)
                print(r.json())

            elif (op == 'Listar produto'):
                id = int(input('\nDigite o id do produto buscado: '))
                # r = requests.get(api_produto)
                # print(r.json())

            print()

            resposta: dict = inquirer.prompt(menu)

        print(msg_sair)

    except KeyboardInterrupt:
        print(msg_sair)


if __name__ == "__main__":
    main()
