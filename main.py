import gradio as gr
import os
import shutil
from pathlib import Path
from rag_utils import create_vector_index, load_vector_index, check_files_changed
from config import (
    DOCUMENTS_DIR, SUPPORTED_EXTENSIONS, 
    TOP_K_RESULTS, MAX_DISPLAY_TEXT_LENGTH,
    APP_TITLE, APP_DESCRIPTION,
    SIMILARITY_THRESHOLD
)
from extractors import get_file_extractor

def process_files(files):
    """Обрабатывает загруженные файлы и сохраняет их в хранилище"""
    try:
        Path(DOCUMENTS_DIR).mkdir(exist_ok=True)
        
        for file_path in files:
            file_name = os.path.basename(file_path)
            ext = os.path.splitext(file_name)[1].lower()
            
            if ext in SUPPORTED_EXTENSIONS:
                dest_path = os.path.join(DOCUMENTS_DIR, file_name)
                shutil.copy2(file_path, dest_path)
        
        if check_files_changed():
            create_vector_index()
            return f"Обработано {len(files)} файлов. Индекс обновлён."
        return f"Обработано {len(files)} файлов. Индекс актуален."

    except Exception as e:
        return f"Ошибка обработки файлов: {str(e)}"

def answer_query(query):
    """Отвечает на пользовательский запрос"""
    if check_files_changed():
        create_vector_index()
    
    index = load_vector_index()
    if not index:
        return "Индекс не найден. Сначала загрузите документы."
    
    query_engine = index.as_query_engine(
        similarity_top_k=TOP_K_RESULTS,
        llm=None,
        response_mode="no_text"
    )
    response = query_engine.query(query)
    
    if not response.source_nodes:
        return "❌ По вашему запросу ничего не найдено"
    
    results = []
    for i, node in enumerate(response.source_nodes, 1):
        # Фильтрация по порогу релевантности
        if node.score < SIMILARITY_THRESHOLD:
            continue
            
        file_name = node.metadata.get("file_name", "Неизвестный файл")
        text = node.text[:MAX_DISPLAY_TEXT_LENGTH] 
        if len(node.text) > MAX_DISPLAY_TEXT_LENGTH:
            text += "..."
        
        results.append(
            f"🔍 Результат #{i}\n"
            f"📄 Файл: {file_name}\n"
            f"⭐ Релевантность: {node.score:.4f}\n"
            f"{'-'*50}\n"
            f"{text}\n\n"
        )
    
    if not results:
        return "❌ Нет результатов, соответствующих порогу релевантности"
    
    return "\n".join(results)

# Интерфейс Gradio
with gr.Blocks(title=APP_TITLE) as demo:
    gr.Markdown(f"# {APP_TITLE}")
    gr.Markdown(APP_DESCRIPTION)

    with gr.Tab("Загрузка документов"):
        file_input = gr.File(
            label=f"Поддерживаемые форматы: {', '.join(SUPPORTED_EXTENSIONS)}",
            file_types=list(SUPPORTED_EXTENSIONS),
            file_count="multiple"
        )
        process_btn = gr.Button("Обработать документы")
        process_output = gr.Textbox(label="Статус обработки", interactive=False)

    with gr.Tab("Поиск"):
        query_input = gr.Textbox(label="Введите ваш запрос", lines=2)
        query_output = gr.Textbox(
            label=f"Топ-{TOP_K_RESULTS} результатов",
            interactive=False,
            lines=10
        )
        search_btn = gr.Button("Найти")

    process_btn.click(process_files, inputs=[file_input], outputs=[process_output])
    search_btn.click(answer_query, inputs=[query_input], outputs=[query_output])

if __name__ == "__main__":
    demo.launch()