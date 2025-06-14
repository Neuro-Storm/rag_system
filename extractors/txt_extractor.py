def extract_text_from_txt(file_path: str) -> str:
    """Извлечение текста из TXT"""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()
    except Exception as e:
        print(f"Ошибка при обработке TXT: {e}")
        return ""