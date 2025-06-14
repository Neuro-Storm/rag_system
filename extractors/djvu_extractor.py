import subprocess

def extract_text_from_djvu(file_path: str) -> str:
    """Извлечение текста из DJVU с помощью djvutxt"""
    try:
        result = subprocess.run(
            ["djvutxt", file_path],
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='ignore'
        )
        return result.stdout
    except Exception as e:
        print(f"Ошибка обработки DJVU: {str(e)}")
        return ""