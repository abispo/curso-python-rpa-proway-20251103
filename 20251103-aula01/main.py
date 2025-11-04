"""
Script que faz o download de arquivos de um servidor FTP, salva os dados em um banco de dados, cria um arquivo zip a partir dos arquivos que foram baixados e envia esse arquivo por e-mail.
"""

import os

from ftplib import FTP

from dotenv import load_dotenv

# Essa função carrega o conteúdo do arquivo .env e o transforma em variáveis de ambiente que ficarão disponíveis durante a execução do script
load_dotenv()

# Baixar os arquivos do FTP
# Ler os arquivos e salvar os dados no banco de dados
# Criar um arquivo zip a partir dos arquivos baixados
# Enviar o arquivo zip por e-mail

def create_downloads_dir():

    # os.getcwd(): Método que retorna o diretório atual de onde o script está sendo executado
    # os.path.join: Método que "combina" os caminhos informados. No caso abaixo, vai retornar o caminho completo até a pasta downloads dentro da pasta do projeto
    downloads_dir = os.path.join(os.getcwd(), "downloads")
    
    # O método os.path.exists verifica se um arquivo/diretório existe
    if not os.path.exists(downloads_dir):

        # O método os.mkdir cria o diretório. Caso o diretório já exista, essa linha lançará uma exceção
        os.mkdir(downloads_dir)

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

if __name__ == "__main__":
    create_downloads_dir()
    download_ftp_files()

    def nao_carrega():
        return True