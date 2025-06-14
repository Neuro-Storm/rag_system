import os
import glob

# Основные файлы проекта
main_files = [
    'main.py',
    'rag_utils.py',
    'config.py'
]

# Файлы экстракторов
extractor_files = [
    'extractors/__init__.py',
    'extractors/common.py',
    'extractors/djvu_extractor.py',
    'extractors/docx_extractor.py',
    'extractors/image_extractor.py',
    'extractors/pdf_extractor.py',
    'extractors/pptx_extractor.py',
    'extractors/txt_extractor.py',
    'extractors/xlsx_extractor.py'
]

# Создаем выходной файл
with open('rag_project_full_code.txt', 'w', encoding='utf-8') as outfile:
    # Обрабатываем основные файлы
    for file_path in main_files:
        outfile.write(f"\n{'='*80}\n")
        outfile.write(f"# ФАЙЛ: {file_path}\n")
        outfile.write(f"{'='*80}\n\n")
        
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as infile:
                outfile.write(infile.read())
                outfile.write("\n\n")
        else:
            outfile.write(f"!!! ФАЙЛ НЕ НАЙДЕН: {file_path} !!!\n\n")
    
    # Обрабатываем файлы экстракторов
    outfile.write(f"\n{'='*80}\n")
    outfile.write(f"# ПАПКА EXTRACTORS\n")
    outfile.write(f"{'='*80}\n\n")
    
    for file_path in extractor_files:
        outfile.write(f"\n{'-'*60}\n")
        outfile.write(f"# Файл: {file_path}\n")
        outfile.write(f"{'-'*60}\n\n")
        
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as infile:
                outfile.write(infile.read())
                outfile.write("\n\n")
        else:
            outfile.write(f"!!! ФАЙЛ НЕ НАЙДЕН: {file_path} !!!\n\n")

print("Все файлы проекта объединены в rag_project_full_code.txt")