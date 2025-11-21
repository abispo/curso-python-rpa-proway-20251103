import datetime
import keyboard
import pyautogui

from time import sleep

pyautogui.PAUSE = 1
pyautogui.FAILSAFE = True

if __name__ == "__main__":
    pyautogui.hotkey("win", "r")

    pyautogui.write("notepad", interval=0.1)
    pyautogui.press("enter")
    sleep(1)

    keyboard.press_and_release("alt+tab")
    sleep(1)
    pyautogui.click()
    pyautogui.scroll(10000)

    sleep(1)

    keyboard.press_and_release("ctrl+a")
    sleep(1)

    keyboard.press_and_release("ctrl+c")
    sleep(1)

    keyboard.press_and_release("alt+tab")
    sleep(1)

    keyboard.press_and_release("ctrl+v")
    sleep(1)

    keyboard.press_and_release("ctrl+s")
    data_hora = datetime.datetime.now(datetime.UTC).strftime("%Y%m%d%H%M%S")
    nome_arquivo = f"{data_hora}_automation.txt"

    keyboard.write(nome_arquivo, delay=0.1)
    sleep(1)
    keyboard.press_and_release("alt+l")

    pyautogui.screenshot(f"{data_hora}_evidencia.png", region=(100, 100, 600, 600))
    sleep(1)
    keyboard.press_and_release("alt+f4")