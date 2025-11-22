import pyautogui
from time import sleep

pyautogui.PAUSE = 0.1
pyautogui.FAILSAFE = True

if __name__ == "__main__":
    sleep(5)

    botao = pyautogui.locateOnScreen("cebolinha.png", confidence=0.5)
    centro_botao = pyautogui.center(botao)

    for numero in range(50):
        pyautogui.click(centro_botao)
        print(f"Clique {numero}!")

# Open CV => Open Computer Vision