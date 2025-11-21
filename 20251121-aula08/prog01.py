
import pyautogui

# A constante PAUSE define o intervalo de tempo entre as chamadas do PyAutoGui
pyautogui.PAUSE = 1.5

# Caso o mouse seja movido para o canto superior esquerdo, será lançada uma exceção
pyautogui.FAILSAFE = True

if __name__ == "__main__":

    # A função size() retorna uma tupla, com os valores de altura e largura da tela
    altura_tela, largura_tela = pyautogui.size()
    print(f"Altura da tela: {altura_tela}.")
    print(f"Largura da tela: {largura_tela}.")

    # A função position() retorna a posição do mouse no eixo x,y.
    eixo_x_mouse, eixo_y_mouse = pyautogui.position()
    print(f"Posição X do mouse: {eixo_x_mouse}.")
    print(f"Posição Y do mouse: {eixo_y_mouse}.")

    # 20, 104
    pyautogui.moveTo(20, 104, duration=2, tween=pyautogui.easeInQuint)
    pyautogui.click()
    
    pyautogui.moveTo(altura_tela/2, largura_tela/2, duration=2)
    pyautogui.click()
    pyautogui.scroll(-1000)
    pyautogui.scroll(1000)

    # 138, 376
    pyautogui.moveRel(-600, -200, duration=3)
    pyautogui.press("esc")
    pyautogui.dragTo(700, 560, duration=3)