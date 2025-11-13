import csv
import requests
from bs4 import BeautifulSoup

URL = "https://defesacivil.riodosul.sc.gov.br/index.php?r=externo%2Fmetragem"

if __name__ == "__main__":
     
    response = requests.get(url=URL, verify=False)
    soup = BeautifulSoup(response.text, "html.parser")

    div_w0 = soup.find("div", {"id": "w0"}).find("table").find("thead").find("tr").find_all("th")

    lista_tags = []
    for tag in div_w0:
        lista_tags.append(tag.get_text())

    print(lista_tags)
    # writerow(lista_tags)

    tbody = soup.find("div", {"id": "w0"}).find("table").find("tbody")

    linhas = []
    for tr in tbody.find_all("tr"):
        
        colunas = []
        for td in tr:
            colunas.append(td.get_text())
        linhas.append(colunas)

    print(linhas)

    with open("dados_rio.csv", "w", encoding="utf-8", newline="") as arquivo:
        arquivo_csv = csv.writer(arquivo, delimiter=';')

        arquivo_csv.writerow(lista_tags)
        arquivo_csv.writerows(linhas)
