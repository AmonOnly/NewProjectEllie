import pyautogui
import time
import pyautogui
import pytesseract
from PIL import ImageGrab

def click(x, y):
    pyautogui.moveTo(x, y)
    pyautogui.click()

def type_text(text):
    pyautogui.typewrite(text)
    pyautogui.press("enter")
def click_text(target_text):
    """
    Procura o texto na tela e clica no centro do primeiro resultado encontrado.
    """
    # captura a tela inteira
    screenshot = ImageGrab.grab()
    ocr_data = pytesseract.image_to_data(screenshot, output_type=pytesseract.Output.DICT)

    for i, word in enumerate(ocr_data['text']):
        if target_text.lower() in word.lower():
            # coordenadas do bloco
            x = ocr_data['left'][i] + ocr_data['width'][i] // 2
            y = ocr_data['top'][i] + ocr_data['height'][i] // 2
            pyautogui.click(x, y)
            return f"Cliquei em '{word}' na tela."
    
    return f"Não encontrei o texto '{target_text}' na tela."