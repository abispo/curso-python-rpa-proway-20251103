import csv
from typing import List

import requests
from bs4 import BeautifulSoup
from bs4.element import ResultSet

URL = "https://defesacivil.riodosul.sc.gov.br/index.php?r=externo%2Fmetragem"

def extract_header(data: ResultSet) -> List[str]:
    return [header.text for header in data]

def extract_values(data: ResultSet) -> List[str]:
    return [[column.text for column in line.find_all("td")] for line in data]

def save_csv(filename: str, data: List[List[str]]):
    with open(file=filename, mode='w', encoding="utf-8", newline="") as _file:
        csv_file = csv.writer(_file, delimiter=';')
        csv_file.writerows(data)

def process_data(soup: BeautifulSoup, element_id: str) -> List[List[str]]:
    # Procuramos uma div usando o id passado como parâmetro
    div = soup.find("div", {"id": element_id})
    table = div.find("table")
    table_body = table.find("tbody")

    # Pegamos os dados para o cabeçalho do arquivo .csv
    table_headers = table.find("thead").find("tr").find_all("th")
    # Pegamos os dados para os values no arquivo .csv
    table_body_lines = table_body.find_all("tr")

    # Abaixo tratamos os dados para montar o retorno da função
    header = extract_header(table_headers)
    values = extract_values(table_body_lines)
    values.insert(0, header)

    return values

def main():
    try:
        # Aqui definimos os cabeçalhos enviados para o servidor. É recomendável pois com isso é mais difícil o site identificar que a requisição é automatizada
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }

        response = requests.get(url=URL, headers=headers, verify=False)

        # Caso aconteça algum erro, lança uma exceção HTTPError
        response.raise_for_status()

        # Criamos o objeto beautifulsoup, que iremos usar para "parsear" a página
        soup = BeautifulSoup(response.text, "html.parser")

        river_data_values = process_data(soup=soup, element_id="w0")
        ituporanga_dam_values = process_data(soup=soup, element_id="w1")
        taio_dam_values = process_data(soup=soup, element_id="w2")

        save_csv("river_data.csv", river_data_values)
        save_csv("ituporanga_dam_data.csv", ituporanga_dam_values)
        save_csv("taio_dam_values.csv", taio_dam_values)

    except Exception as e:
        print(f"Erro ao processar a requisição: {e}.")

if __name__ == "__main__":
    main()