import csv
import os

"""
Salvando arquivos .csv

Podemos salvar arquivos .csv pelo Python de 2 maneiras: Utilizando a função writer, ou a classe DictWriter.

Quando utilizamos a função writer, passamos uma lista de valores que será salva como a linha do arquivo .csv Já com DictWriter, passamos um dicionário, onde as chaves desse dicionário serão os nomes das colunas, e os valores, os valores das linhas.
"""

if __name__ == "__main__":
    
    dados = [
        ["Introdução ao Java", 30, 500],
        ["Python com Banco de Dados", 28, 350],
        ["Microserviços com Go", 40, 800]
    ]

    with open("cursos.csv", "w", encoding="utf-8", newline="") as arquivo:

        arquivo_csv = csv.writer(arquivo, delimiter=';')
        # O método writerow salva uma linha no arquivo, recebendo uma lista de valores
        arquivo_csv.writerow(["Nome do Curso", "Preço", "Carga Horária"])

        # O método writerows salva várias linhas no arquivo de uma vez só. O parâmetro passado deve ser uma lista de listas (ou um iterável de iteráveis)
        arquivo_csv.writerows(dados)

    with open("clientes.csv", "w", encoding="utf-8", newline="") as arquivo:

        # A classe DictWriter recebe um segundo parâmetro chamado fieldnames, onde passamos o nome das colunas do arquivo, como uma lista de strings.
        arquivo_csv = csv.DictWriter(
            arquivo,
            ["Nome", "Data de Nascimento", "Gênero"],
            delimiter=';'
        )

        arquivo_csv.writeheader()

        arquivo_csv.writerow({
            "Nome": "João da Silva",
            "Data de Nascimento": "2000-04-05",
            "Gênero": "Masculino"
        })

        clientes = [
            {"Nome": "Maria das Graças", "Data de Nascimento": "1998-07-13", "Gênero": "Feminino"},
            {"Nome": "Paulo Chagas", "Data de Nascimento": "1995-02-11", "Gênero": "Masculino"},
            {"Nome": "Amanda Costa", "Data de Nascimento": "1991-10-22", "Gênero": "Feminino"},
        ]

        arquivo_csv.writerows(clientes)

    # pip install requests beautifulsoup4