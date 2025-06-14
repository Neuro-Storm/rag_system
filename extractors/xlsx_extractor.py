import pandas as pd

def extract_text_from_xlsx(file_path: str) -> str:
    """Извлечение текста из Excel"""
    try:
        text = []
        xl = pd.ExcelFile(file_path)
        for sheet_name in xl.sheet_names:
            df = xl.parse(sheet_name)
            text.append(df.to_string())
        return "\n".join(text)
    except Exception as e:
        print(f"Ошибка чтения Excel: {str(e)}")
        return ""