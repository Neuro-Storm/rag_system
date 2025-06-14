from PIL import Image
import pytesseract

def extract_text_from_image(file_path: str) -> str:
    """Извлечение текста из изображений с помощью Tesseract"""
    try:
        img = Image.open(file_path)
        return pytesseract.image_to_string(img, lang='rus+eng')
    except Exception as e:
        print(f"Ошибка OCR: {str(e)}")
        return ""