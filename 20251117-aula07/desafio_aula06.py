"""
Você irá acessar o site https://saucedemo.com, e efetuar o login (pode usar os nomes de usuários e senha que estão informados na própria página)
Depois que logar no site, você irá colocar 2 itens no carrinho, e depois irá acessar o carrinho.
Após isso, irá clicar no botão checkout e preencher as informações no formulário.
Depois das informações preenchidas, você irá clicar no botão Continue.
Após isso você irá para a página de visualização do checkout.
Você deve mostrar no terminal os itens que você colocou no carrinho, os valores de Payment Information e Shipping Information e por final o preço total, com a taxa inclusa.

"""

from time import sleep

from fake_useragent import UserAgent

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

ua = UserAgent()

options = ChromeOptions()
options.page_load_strategy = "eager"
options.add_argument("--headless")
options.add_argument("--window-size=1920,1080")
options.add_argument("--start-maximized")
options.add_argument(f"--user-agent={ua.firefox}")
options.add_experimental_option("prefs", prefs)

if __name__ == "__main__":
    url = "https://www.saucedemo.com/"

    driver = webdriver.Chrome(
        service=ChromeService(
            ChromeDriverManager().install()
        ),
        options=options
    )

    print("Acessando o site...")
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

    tshirt_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "add-to-cart-sauce-labs-bolt-t-shirt"))
    )
    tshirt_button.click()
    sleep(1.5)

    fleece_jacket_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "add-to-cart-sauce-labs-fleece-jacket"))
    )
    fleece_jacket_button.click()
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

    quantities_list = driver.find_elements(By.XPATH, "//div[@class='cart_quantity']")
    names_list = driver.find_elements(By.XPATH, "//div[@class='inventory_item_name']")
    prices_list = driver.find_elements(By.XPATH, "//div[@class='inventory_item_price']")
    
    # Corrigir para uma lista para cada valor
    for index in range(len(cart_items)):
        quantity = quantities_list[index].text
        name = names_list[index].text
        price = prices_list[index].text
        
        line = f"{quantity.ljust(5)}{name.ljust(30)}{price.ljust(10)}"
        print(line)

    summary_values = driver.find_elements(By.CLASS_NAME, "summary_value_label")
    summary_total = driver.find_element(By.CLASS_NAME, "summary_total_label")
    summary_tax = driver.find_element(By.CLASS_NAME, "summary_tax_label")

    print(f"\n\nInformação de Entrega: {summary_values[1].text}")
    print(f"Informação de Pagamento: {summary_values[0].text}")
    print(f"Taxa: {summary_tax.text.split()[-1]}")
    print(f"Preço total: {summary_total.text.split()[-1]}\n")

    driver.save_screenshot("photo.png")
    driver.quit()
