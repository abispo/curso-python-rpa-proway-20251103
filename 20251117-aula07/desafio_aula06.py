"""
Você irá acessar o site https://saucedemo.com, e efetuar o login (pode usar os nomes de usuários e senha que estão informados na própria página)
Depois que logar no site, você irá colocar 2 itens no carrinho, e depois irá acessar o carrinho.
Após isso, irá clicar no botão checkout e preencher as informações no formulário.
Depois das informações preenchidas, você irá clicar no botão Continue.
Após isso você irá para a página de visualização do checkout.
Você deve mostrar no terminal os itens que você colocou no carrinho, os valores de Payment Information e Shipping Information e por final o preço total, com a taxa inclusa.

"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

options = ChromeOptions()
options.page_load_strategy = "eager"
options.add_argument("--start-maximized")

if __name__ == "__main__":
    url = "https://www.saucedemo.com/"

    driver = webdriver.Chrome(
        service=ChromeService(
            ChromeDriverManager().install()
        ),
        options=options
    )

    driver.get(url=url)

    login_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "login-box"))
    )

    login_button = driver.find_element(By.ID, "user-name")

    driver.quit()