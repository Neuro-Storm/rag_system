import json
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

def process_files(files: list[str]) -> dict:
    """
    Обрабатывает загруженные файлы и обновляет векторный индекс при необходимости.

    Args:
        files (list[str]): Пути к загруженным файлам

    Returns:
        dict: Статус обработки и информация об индексе
    """
    try:
        Path(DOCUMENTS_DIR).mkdir(exist_ok=True)
        saved_count = 0
        for file_path in files:
            file_name = os.path.basename(file_path)
            ext = os.path.splitext(file_name)[1].lower()
            if ext in SUPPORTED_EXTENSIONS:
                dest = os.path.join(DOCUMENTS_DIR, file_name)
                shutil.copy2(file_path, dest)
                saved_count += 1
        # Проверить изменения
        updated = False
        if check_files_changed():
            create_vector_index()
            updated = True
        status = f"Обработано {saved_count} файлов"
        status += ". Индекс обновлён." if updated else ". Индекс актуален."
        return {"status": status, "updated_index": updated}
    except Exception as e:
        return {"status": f"Ошибка: {str(e)}", "updated_index": False}

def answer_query(query: str) -> dict:
    """
    Выполняет поиск по векторному индексу и возвращает результаты.

    Args:
        query (str): Текст запроса

    Returns:
        dict: Список результатов с метаданными
    """
    # Обновить индекс при изменениях
    if check_files_changed():
        create_vector_index()
    index = load_vector_index()
    if not index:
        return {"results": [], "message": "Индекс не найден. Загрузите документы."}

    query_engine = index.as_query_engine(
        similarity_top_k=TOP_K_RESULTS,
        llm=None,
        response_mode="no_text"
    )
    response = query_engine.query(query)
    nodes = response.source_nodes or []
    results = []
    for node in nodes:
        if node.score < SIMILARITY_THRESHOLD:
            continue
        snippet = node.text[:MAX_DISPLAY_TEXT_LENGTH]
        if len(node.text) > MAX_DISPLAY_TEXT_LENGTH:
            snippet += "..."
        results.append({
            "file": node.metadata.get("file_name", "unknown"),
            "score": round(node.score, 4),
            "snippet": snippet
        })
    if not results:
        return {"results": [], "message": "Нет релевантных результатов."}
    return {"results": results}

# Создание интерфейса Gradio с поддержкой MCP
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
        process_output = gr.JSON(label="Статус обработки")

    with gr.Tab("Поиск"):
        query_input = gr.Textbox(label="Введите ваш запрос", lines=2)
        search_btn = gr.Button("Найти")
        query_output = gr.JSON(label=f"Топ-{TOP_K_RESULTS} результатов")

    process_btn.click(process_files, inputs=[file_input], outputs=[process_output])
    search_btn.click(answer_query, inputs=[query_input], outputs=[query_output])

if __name__ == "__main__":
    demo.launch(mcp_server=True)