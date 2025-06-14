def extract_text_common(file_path: str) -> str:
    """Обработка текстовых форматов"""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()
    except Exception as e:
        print(f"Ошибка чтения {file_path}: {str(e)}")
        return ""