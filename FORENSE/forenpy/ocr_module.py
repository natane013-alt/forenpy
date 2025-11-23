import pytesseract
from PIL import Image

def ocr_image(path: str, lang: str = 'por') -> str:
    img = Image.open(path)
    text = pytesseract.image_to_string(img, lang=lang)
    return text
