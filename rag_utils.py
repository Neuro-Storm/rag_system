import os
import pickle
import hashlib
import faiss
import torch
from pathlib import Path
from llama_index.core import Settings, VectorStoreIndex
from llama_index.core.schema import Document
from llama_index.core.ingestion import IngestionPipeline
from llama_index.core.node_parser import SentenceSplitter
from llama_index.vector_stores.faiss import FaissVectorStore
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core.storage.storage_context import StorageContext
from llama_index.core import load_index_from_storage
from config import (
    DOCUMENTS_DIR, INDEX_DIR, SUPPORTED_EXTENSIONS, 
    EMBED_MODEL, VECTOR_DIMENSION, EMBED_BATCH_SIZE,
    CHUNK_SIZE, CHUNK_OVERLAP
)
from extractors import get_file_extractor

# Отключаем LLM и настраиваем эмбеддинги
Settings.llm = None
Settings.embed_model = HuggingFaceEmbedding(
    model_name=EMBED_MODEL,
    device="cuda" if torch.cuda.is_available() else "cpu",
    embed_batch_size=EMBED_BATCH_SIZE
)
Settings.chunk_size = CHUNK_SIZE
Settings.chunk_overlap = CHUNK_OVERLAP

STATE_FILE = Path(INDEX_DIR) / ".file_state.pkl"
FILE_EXTRACTOR = get_file_extractor()

def ensure_directories():
    Path(DOCUMENTS_DIR).mkdir(parents=True, exist_ok=True)
    Path(INDEX_DIR).mkdir(parents=True, exist_ok=True)

def calculate_file_hash(path: str) -> str:
    with open(path, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()

def save_file_state(file_hashes: dict):
    with open(STATE_FILE, "wb") as f:
        pickle.dump({
            "timestamp": os.path.getmtime(STATE_FILE) if STATE_FILE.exists() else 0,
            "file_hashes": file_hashes
        }, f)

def load_file_state():
    if not STATE_FILE.exists():
        return {}
    with open(STATE_FILE, "rb") as f:
        return pickle.load(f).get("file_hashes", {})

def check_files_changed() -> bool:
    """Проверяет изменения в документах"""
    ensure_directories()
    current_hashes = {}
    
    for file in Path(DOCUMENTS_DIR).iterdir():
        if file.is_file() and file.suffix.lower() in SUPPORTED_EXTENSIONS:
            current_hashes[file.name] = calculate_file_hash(file)
    
    saved_hashes = load_file_state()
    return current_hashes != saved_hashes

def create_vector_index():
    """Создает векторный индекс из документов"""
    try:
        ensure_directories()
        documents = []
        
        # Чтение и обработка документов
        for file_path in Path(DOCUMENTS_DIR).iterdir():
            if not file_path.is_file() or file_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
                continue
            
            extractor = FILE_EXTRACTOR.get(file_path.suffix.lower())
            if extractor:
                try:
                    doc_content = extractor(str(file_path))
                    documents.append(Document(
                        text=doc_content,
                        metadata={"file_name": file_path.name}
                    ))
                except Exception as e:
                    print(f"Ошибка обработки {file_path}: {str(e)}")
        
        if not documents:
            print("Нет документов для индексации.")
            return None
        
        # Создание пайплайна обработки
        pipeline = IngestionPipeline(
            transformations=[
                SentenceSplitter(chunk_size=Settings.chunk_size, chunk_overlap=Settings.chunk_overlap)
            ]
        )
        nodes = pipeline.run(documents=documents)
        
        # Создание FAISS индекса
        faiss_index = faiss.IndexFlatL2(VECTOR_DIMENSION)
        vector_store = FaissVectorStore(faiss_index=faiss_index)
        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        
        # Построение и сохранение индекса
        index = VectorStoreIndex(nodes, storage_context=storage_context)
        index.storage_context.persist(persist_dir=INDEX_DIR)
        
        # Сохранение состояния файлов
        save_file_state({
            file.name: calculate_file_hash(file) 
            for file in Path(DOCUMENTS_DIR).iterdir() 
            if file.is_file()
        })
        
        print("✅ Векторный индекс успешно создан.")
        return index

    except Exception as e:
        print(f"❌ Ошибка создания индекса: {str(e)}")
        return None

def load_vector_index():
    """Загружает векторный индекс"""
    try:
        ensure_directories()
        
        if not any(Path(INDEX_DIR).iterdir()):
            return None
        
        # Загрузка FAISS индекса
        vector_store = FaissVectorStore.from_persist_dir(INDEX_DIR)
        storage_context = StorageContext.from_defaults(
            vector_store=vector_store,
            persist_dir=INDEX_DIR
        )
        
        index = load_index_from_storage(storage_context)
        print("✅ Индекс успешно загружен.")
        return index

    except Exception as e:
        print(f"❌ Ошибка загрузки индекса: {str(e)}")
        return None