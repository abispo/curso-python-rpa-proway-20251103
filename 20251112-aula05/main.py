import datetime
import os
import requests
import sqlite3

from sqlite3 import Connection
from typing import List, Tuple

from bs4 import BeautifulSoup
from bs4.element import Tag

URL = "https://defesacivil.blumenau.sc.gov.br/d/nivel-do-rio"

def configure_database(connection: Connection):
    sql = """
CREATE TABLE IF NOT EXISTS tb_leitura_rio_blumenau(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data_hora TEXT UNIQUE NOT NULL,
    nivel REAL NOT NULL,
    variacao TEXT NOT NULL
);"""

    cursor = connection.cursor()
    cursor.execute(sql)


def clean_data(columns: List[Tag]) -> Tuple[str]:

    date_time = datetime.datetime.strptime(
        columns[0].get_text().strip(),
        "%d/%m/%Y %H:%M"
    ).strftime("%Y-%m-%d %H:%M:%S")
    level = columns[1].get_text().strip().replace(',', '.')
    variation = columns[2].get_text().strip()

    return (date_time, level, variation,)


def save_data(connection: Connection, data: Tuple[str]):
    sql = """
    INSERT INTO tb_leitura_rio_blumenau(data_hora, nivel, variacao) VALUES (?, ?, ?)
    ON CONFLICT(data_hora) DO UPDATE SET
        data_hora = excluded.data_hora,
        nivel = excluded.nivel,
        variacao = excluded.variacao;"""
    cursor = connection.cursor()
    cursor.execute(sql, data)

    connection.commit()
    cursor.close()

    print(f"Registro '{data[0]}' salvo com sucesso.")


if __name__ == "__main__":
    print("Baixando informações do site nivel do rio")

    # Na linha abaixo acessamos a URL passada no parâmetro url da função get do módulo requests. Essa chamada irá retornar um objeto do tipo Response. O parâmetro verify=False indica que não queremos fazer a verificação de certificados SSL do site.
    response = requests.get(url=URL, verify=False)

    # Abaixo estamos instanciando a classe BeautifulSoup, que irá retornar o objeto no qual faremos o processamento do HTML da página que baixamos, utilizando o html.parser
    soup = BeautifulSoup(response.text, "html.parser")

    # Configuração do banco de dados
    connection_string = os.path.join(os.getcwd(), "medidas_rio_blumenau.sqlite3")
    connection = sqlite3.connect(connection_string)
    configure_database(connection)

    # O comando find retorna um objeto do tipo Tag, que representa a tag que buscamos. No caso abaixo, estamos procurando por uma tag <table> que tenha como parâmetro id o valor "river-level-table"
    table = soup.find("table", {"id": "river-level-table"})

    # A linha abaixo procuta a tag <tbody> que faz parte da árvore de elementos da tag <table>. A partir de objetos Tag, é possível fazer uma busca em tags filhas. 
    table_body = table.find("tbody")

    # O método find_all irá retornar um objeto do tipo ResultSet, que representa a lista de tags <tr> que são filhas da tag <tbody>. Esse objeto é iterável. 
    table_lines = table_body.find_all("tr")

    for line in table_lines:
        
        columns = line.find_all("td")
        table_data = clean_data(columns)
        
        save_data(connection, table_data)