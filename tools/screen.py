import mss
import numpy as np
from PIL import Image
import pytesseract

def screenshot():
    with mss.mss() as sct:
        monitor = sct.monitors[1]
        sct_img = sct.grab(monitor)
        img = Image.frombytes("RGB", sct_img.size, sct_img.rgb)
        return img

def read_screen():
    img = screenshot()
    text = pytesseract.image_to_string(img, lang="por")
    return text
