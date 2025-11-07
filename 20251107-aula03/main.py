"""
Script que faz o download de arquivos de um servidor FTP, salva os dados em um banco de dados, cria um arquivo zip a partir dos arquivos que foram baixados e envia esse arquivo por e-mail.
"""

import csv
import datetime
import os
import sqlite3
import zipfile

from ftplib import FTP
from sqlite3 import Connection
from typing import List

from dotenv import load_dotenv

# Essa função carrega o conteúdo do arquivo .env e o transforma em variáveis de ambiente que ficarão disponíveis durante a execução do script
load_dotenv()

# Enviar o arquivo zip por e-mail

def create_database(connection: Connection):

    cursor = connection.cursor()

    sql = """
    CREATE TABLE sensores(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        codigo TEXT UNIQUE NOT NULL
    );"""
    cursor.execute(sql)

    sql = """
    CREATE TABLE leituras(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_sensor INTEGER NOT NULL,
        tipo TEXT NOT NULL,
        data_hora TEXT NOT NULL,
        valor REAL NOT NULL,
        unidade TEXT NULL,
        FOREIGN KEY(id_sensor) REFERENCES sensores(id));"""
    cursor.execute(sql)

    print("Banco de dados criado com sucesso.")

def create_downloads_dir():

    # os.getcwd(): Método que retorna o diretório atual de onde o script está sendo executado
    # os.path.join: Método que "combina" os caminhos informados. No caso abaixo, vai retornar o caminho completo até a pasta downloads dentro da pasta do projeto
    downloads_dir = os.path.join(os.getcwd(), "downloads")
    
    # O método os.path.exists verifica se um arquivo/diretório existe
    if not os.path.exists(downloads_dir):

        # O método os.mkdir cria o diretório. Caso o diretório já exista, essa linha lançará uma exceção
        os.mkdir(downloads_dir)

# Baixar os arquivos do FTP
def download_ftp_files():

    itens = []
    
    with FTP(os.getenv("FTP_HOST")) as ftp:
        
        # Login no servidor
        ftp.login(user=os.getenv("FTP_USER"), passwd=os.getenv("FTP_PASS"))
        
        # Entrar na pasta files, onde estão os diretórios
        ftp.cwd("files")

        # Entrar na pasta do dia 20 de outubro de 2025
        ftp.cwd("20251020")

        # O método retrlines retorna o conteúdo do diretório atual. O segundo parâmetro da função é uma função que será chamada pra cada item que o comando listas. Ou seja, vamos adicionar na lista itens os valores mostrados na listagem da pasta (arquivos)
        ftp.retrlines("LIST", itens.append)
        
        for item in itens:
            filename = item.split(" ")[-1]
            
            with open(os.path.join(os.getcwd(), "downloads", filename), "wb") as ftp_file:
                ftp.retrbinary(f"RETR {filename}", ftp_file.write)
                print(f"Arquivo '{filename}' salvo com sucesso.")

# Ler os arquivos e salvar os dados no banco de dados
def save_data(connection: Connection, filename: str, csv_file: csv.DictReader):
    
    # Aqui a gente retira a extensão do nome do arquivo
    filename = filename.replace(".csv", "")

    # O método split separa a string transformando em uma lista, utilizando um separador
    filename_parts = filename.split("_")

    sensor_name = filename_parts[0]
    sensor_type = filename_parts[1]
    sensor_read_date = filename_parts[2]

    cursor = connection.cursor()

    # O método fetchone do cursor retorna um registro do resultado. Caso não haja registros na consulta, o método retorna None
    result = cursor.execute("SELECT * FROM sensores WHERE codigo = ?", (sensor_name,)).fetchone()
    
    if result:
        sensor_id = result[0]

    else:
        cursor.execute("INSERT INTO sensores(codigo) VALUES (?)", (sensor_name,))
        connection.commit()
        sensor_id = cursor.lastrowid

    for line in csv_file:
        sql = """
        INSERT INTO
            leituras(id_sensor, tipo, data_hora, valor, unidade)
        VALUES
            (?, ?, ?, ?, ?)"""
        
        year = sensor_read_date[:4]
        month = sensor_read_date[4:6]
        day = sensor_read_date[6:]
        hour = line["timestamp"]
        
        timestamp = f"{year}-{month}-{day} {hour}"
        
        cursor.execute(sql, (sensor_id, sensor_type, timestamp, line["valor"], line["unidade"],))
    
    connection.commit()

# Criar um arquivo zip a partir dos arquivos baixados
def create_zipfile(filenames: List[str]):
    
    today = datetime.date.today().strftime(
        "%Y%m%d"
    )

    zipfile_name = f"dados_sensores_{today}.zip"

    with zipfile.ZipFile(zipfile_name, "w", zipfile.ZIP_DEFLATED) as zipf:
        for filename in filenames:
            file_path = os.path.join(os.getcwd(), "downloads", filename)

            zipf.write(file_path, arcname=filename)

    print("Arquivo zip salvo com sucesso.")
    

if __name__ == "__main__":

    # Criamos o objeto de conexão ao banco de dados SQLite
    connection_string = os.path.join(os.getcwd(), "db.sqlite3")

    create_downloads_dir()
    download_ftp_files()

    # Se o arquivo do banco de dados existe, iremos apagá-lo
    if os.path.exists(connection_string):
        os.remove(connection_string)
        print(f"Arquivo '{connection_string}' removido.")

    sqlite_connection = sqlite3.connect(connection_string)
    create_database(connection=sqlite_connection)

    downloads_dir = os.path.join(os.getcwd(), "downloads")

    # A função listdir lista o conteúdo do diretório passado como parâmetro
    filenames = os.listdir(downloads_dir)

    for filename in filenames:
        
        file_path = os.path.join(downloads_dir, filename)

        with open(file_path, "r", encoding="utf-8") as _file:
            csv_file = csv.DictReader(_file, delimiter=';')

            save_data(
                connection=sqlite_connection,
                filename=filename,
                csv_file=csv_file
            )

    create_zipfile(filenames)
