# 🌐 Многоформатная RAG система

Система интеллектуального поиска по документам с использованием векторных индексов.

---

## 🚀 Быстрый старт

### 1. Клонирование репозитория

```bash
git clone https://github.com/Neuro-Storm/rag_system.git
cd rag_system
```

### 2. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 3. Установка djvulibre-bin

- **Windows** (через Chocolatey):

    ```bash
    choco install djvu-libre -y
    ```

- **Linux** (пример):

    ```bash
    sudo apt-get install djvulibre-bin
    ```

---

## ▶️ Использование

Запустите приложение:

```bash
python main.py
```

Откройте в браузере:

[http://localhost:7860](http://localhost:7860)

---

## 📄 Поддерживаемые форматы

**Документы:**  
`PDF`, `DOCX`, `PPTX`, `XLSX`

**Текстовые:**  
`TXT`, `CSV`, `HTML`, `MD`

**Изображения:**  
`JPG`, `PNG`, `JPEG`

**DJVU**

---

## ⚙️ Конфигурация

Настройки можно изменить в файле `config.py`:

- **Количество результатов:**  
  `TOP_K_RESULTS = 5`

- **Длина отображаемого текста:**  
  `MAX_DISPLAY_TEXT_LENGTH = 2000`

- **Размер фрагментов документа:**  
  `CHUNK_SIZE = 1024`

---
