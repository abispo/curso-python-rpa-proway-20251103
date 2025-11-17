from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

# Se quisermos utilizar opções do navegador, utilizamos a classe Option
options = ChromeOptions()
options.page_load_strategy = "eager"
options.add_argument("--start-maximized")

URL = "https://www.proway.com.br/"

if __name__ == "__main__":
    # Aqui instanciamos o navegador com as opções
    driver = webdriver.Chrome(
        service=ChromeService(
            ChromeDriverManager().install()
        ),
        options=options
    )

    # O método get acessa uma URL. Se o navegador não estiver sendo executado, esse comando o executa.
    driver.get(URL)

    sleep(2)

    texto_busca = driver.find_element(By.ID, "termoBuscaCurso")
    texto_busca.send_keys("Python")
    
    # Simulando o pressionamento da tecla ENTER
    # texto_busca.send_keys(Keys.ENTER)

    # Simulando o clique do mouse no botão de busca
    botao_buscar = driver.find_element(By.NAME, "buscar")
    botao_buscar.click()

    link_moda_textil = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.LINK_TEXT, "Moda e Têxtil"))
    )
    link_moda_textil.click()

    div_lista_cursos = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "listaCursos"))
    )

    lista_cursos = driver.find_elements(By.XPATH, "//div[@class='sombra']//h2")
    print("=== LISTA DOS CURSOS DE MODA E TÊXTIL DA PROWAY ===")

    for curso in lista_cursos:
        print(curso.text)

    sleep(3)
    driver.quit()