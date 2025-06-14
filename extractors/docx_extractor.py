try:
    # Попробуем импортировать из правильного пакета
    from docx import Document
except ImportError:
    # Альтернативная реализация для извлечения текста из DOCX
    import zipfile
    import xml.etree.ElementTree as ET

    def extract_text_from_docx(file_path: str) -> str:
        """Извлечение текста из DOCX с помощью чистого Python"""
        try:
            text = []
            # Открываем DOCX как ZIP-архив
            with zipfile.ZipFile(file_path) as docx:
                # Читаем основной документ
                xml_content = docx.read('word/document.xml')
                root = ET.fromstring(xml_content)
                
                # Пространство имен XML
                ns = {
                    'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
                }
                
                # Ищем все текстовые элементы
                for paragraph in root.findall('.//w:p', ns):
                    para_text = []
                    for run in paragraph.findall('.//w:r', ns):
                        for text_elem in run.findall('.//w:t', ns):
                            para_text.append(text_elem.text)
                    text.append(''.join(para_text))
                    
            return '\n'.join(text)
        except Exception as e:
            print(f"Ошибка чтения DOCX: {str(e)}")
            return ""
else:
    def extract_text_from_docx(file_path: str) -> str:
        """Извлечение текста из DOCX с помощью python-docx"""
        try:
            doc = Document(file_path)
            return "\n".join([para.text for para in doc.paragraphs])
        except Exception as e:
            print(f"Ошибка чтения DOCX: {str(e)}")
            return ""