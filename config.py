import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOCUMENTS_DIR = os.path.join(BASE_DIR, "documents")
INDEX_DIR = os.path.join(BASE_DIR, "index_store")

SUPPORTED_EXTENSIONS = {
    ".pdf", ".txt", ".docx", ".pptx", 
    ".xlsx", ".csv", ".jpg", ".png", 
    ".jpeg", ".html", ".md", ".djvu"
}

# Настройки модели
EMBED_MODEL = "Qwen/Qwen3-Embedding-0.6B"
VECTOR_DIMENSION = 1024
EMBED_BATCH_SIZE = 2

# Настройки обработки документов
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

# Настройки поиска
TOP_K_RESULTS = 5
MAX_DISPLAY_TEXT_LENGTH = 1500
SIMILARITY_THRESHOLD = 0.9  # Порог релевантности (0-1)

# Настройки интерфейса
APP_TITLE = "📄 Многоформатный RAG с поиском по документам"
APP_DESCRIPTION = "Система поиска по документам с использованием векторных индексов"