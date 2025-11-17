"""
Você irá acessar o site https://saucedemo.com, e efetuar o login (pode usar os nomes de usuários e senha que estão informados na própria página)
Depois que logar no site, você irá colocar 2 itens no carrinho, e depois irá acessar o carrinho.
Após isso, irá clicar no botão checkout e preencher as informações no formulário.
Depois das informações preenchidas, você irá clicar no botão Continue.
Após isso você irá para a página de visualização do checkout.
Você deve mostrar no terminal os itens que você colocou no carrinho, os valores de Payment Information e Shipping Information e por final o preço total, com a taxa inclusa.

"""

from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

prefs = {
    "profile.password_manager_leak_detection": False,
    "credentials_enable_service": False,
    "profile.password_manager_enabled": False
}

options = ChromeOptions()
options.page_load_strategy = "eager"
options.add_argument("--start-maximized")
options.add_experimental_option("prefs", prefs)

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

    username_text = driver.find_element(By.ID, "user-name")
    username_text.send_keys("standard_user")
    sleep(1)

    password_text = driver.find_element(By.ID, "password")
    password_text.send_keys("secret_sauce")
    sleep(1)

    login_button = driver.find_element(By.ID, "login-button")
    login_button.click()
    sleep(2)

    backpack_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "add-to-cart-sauce-labs-backpack"))
    )
    backpack_button.click()
    sleep(1.5)

    bike_light_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "add-to-cart-sauce-labs-bike-light"))
    )
    bike_light_button.click()
    sleep(1.5)

    shopping_cart_button = driver.find_element(By.ID, "shopping_cart_container")
    shopping_cart_button.click()
    sleep(1.5)

    checkout_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "checkout",))
    )
    checkout_button.click()
    sleep(1.5)

    first_name_text = driver.find_element(By.ID, "first-name")
    first_name_text.send_keys("Alessandro")
    sleep(1.5)

    last_name_text = driver.find_element(By.ID, "last-name")
    last_name_text.send_keys("Bispo")
    sleep(1.5)

    postal_code_text = driver.find_element(By.ID, "postal-code")
    postal_code_text.send_keys("89074-000")
    sleep(1.5)

    continue_button = driver.find_element(By.ID, "continue")
    continue_button.click()
    sleep(1.5)

    cart_items = driver.find_elements(By.CLASS_NAME, "cart_item")

    header = f"{'Qnt'.ljust(5)}{'Item'.ljust(30)}{'Preço'.ljust(10)}"
    header_line = '-'*len(header)

    print(header)
    print(header_line, end='\n\n')
    
    # Corrigir para uma lista para cada valor
    for cart_item in cart_items:
        cart_quantityl = cart_item.find_elements(By.XPATH, "//div[@class='cart_item_label']")
        cart_quantity = cart_item.find_element(By.XPATH, "//div[@class='cart_quantity']").text
        item_name = cart_item.find_element(
            By.XPATH,
            "//div[@class='cart_item_label']//div[@class='inventory_item_name']"
        ).text
        item_price = cart_item.find_element(
            By.XPATH,
            "//div[@class='cart_item_label']//div[@class='item_pricebar']//div[@class='inventory_item_price']"
        ).text.split()[-1]
        # Apesar de ser funcional, podemos passar direto a última classe onde a informação que queremos está. Ou seja, o comando xpath acima poderia ser //div[@class='inventory_item_price']
        
        line = f"{cart_quantity.ljust(5)}{item_name.ljust(30)}{item_price.ljust(10)}"
        print(line)

    driver.quit()
