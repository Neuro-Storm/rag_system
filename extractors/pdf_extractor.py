from PyPDF2 import PdfReader

def extract_text_from_pdf(file_path: str) -> str:
    """Извлечение текста из PDF"""
    try:
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            raw_text = page.extract_text()
            if isinstance(raw_text, bytes):
                text += raw_text.decode('utf-8', errors='replace') + "\n"
            else:
                text += raw_text + "\n"
        return text
    except Exception as e:
        print(f"Ошибка при обработке PDF: {e}")
        return ""