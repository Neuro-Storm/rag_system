# Многоформатная RAG система

Система поиска по документам с использованием векторных индексов.

## Установка

1. Клонируйте репозиторий:
git clone https://github.com/Neuro-Storm/rag_system.git
cd rag_system

2. Установите зависимости:

pip install -r requirements.txt

3. Установите djvulibre-bin, тем или иным способом, например:
	choco install djvu-libre -y   
    
Использование
Запустите приложение:

python main.py
Откройте в браузере: http://localhost:7860

Поддерживаемые форматы
PDF, DOCX, PPTX, XLSX

Текстовые: TXT, CSV, HTML, MD

Изображения: JPG, PNG, JPEG

DJVU

Конфигурация
Настройки можно изменить в config.py:


Количество результатов
TOP_K_RESULTS = 5

Длина отображаемого текста
MAX_DISPLAY_TEXT_LENGTH = 2000

Размер фрагментов документа
CHUNK_SIZE = 1024
