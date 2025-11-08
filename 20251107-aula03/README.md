# Desafio

Você irá criar um script que irá baixar um arquivo de uma URL, descompactar esse arquivo e organizar os arquivos pdf que estavam compactados, em pastas.

Por exemplo: Quando você ler o nome do arquivo (01-10-2025), o script deverá:
* Criar a pasta 2025, caso ela não exista
* Dentro da pasta do ano, criar a pasta 10 (que é o mês) caso não exista
* Copiar o arquivo para essa pasta.

Vocês vão precisar instalar a biblioteca `requests` (`pip install requests`).

Não esqueçam de utilizar um virtual environment (venv). Que pode ser criado pelo vs code (Abrindo a janela de comandos (CTRL+SHIFT+P) e procurando pelo comando Python: Create Environment) ou pelo terminal utilizando o comando `python -m venv .venv`

O endereço onde está o arquivo é http://147.93.4.194/dados_ceasa_sc_2025.zip