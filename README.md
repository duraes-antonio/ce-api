# Intagração de API com WooCommerce

A proposta deste repositório é o desenvolvimento de uma Interface de Programação de Aplicações (API) integrada ao banco
de dados do Sistema de Gestão de Conteúdo (CMS) Wordpress e seu plugin para e-commerce / lojas virtuais, WooCommerce.

Tecnologias
* Python 3.7 (Linguagem de programação escolhida)
* Flask 1.1.2 (Framework web p/ construir API)
* PyMySQL 0.10.0 (Driver para conexão e operações c/ MySQL)
* inquirer 2.7.0 (Biblioteca p/ construção de menu em lista)

## Como configurar o projeto

### Instalação de dependências

Após baixar e instalar o [Python 3.5+](https://www.python.org/downloads/release/python-378/), siga o seguinte algorítimo para instalar suas dependências:
* Abra o terminal, Powershell ou CMD na pasta "src" do projeto;
* Digite o comando "_pip install -r requirements.txt_" (substitua "pip" por "pip3" se seu S.O. for Linux) e dê ENTER

### Conexão com Banco de Dados
É necessário ter um banco rodando com as seguintes configurações
ou alterar o arquivo "config_bd.py" para se adequar ao seu banco MySQL.

Configurações padrão do Banco de Dados:

    "host": "127.0.0.1",
    "port": 3306,
    "user": "root",
    "passwd": "",
    "database": "loja"
 
## Como executar o projeto

### Executar API

* Abra o terminal, Powershell ou CMD na pasta "src" do projeto;
* Digite o comando "python api"* e dê ENTER

### Executar cliente

* Abra um **novo** terminal, Powershell ou CMD na pasta "src" do projeto;
* Digite o comando "python cliente"* e dê ENTER

*Obs.: Substitua "python" por "python3" se seu S.O. for Linux

