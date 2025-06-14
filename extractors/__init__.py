from .common import extract_text_common
from .pdf_extractor import extract_text_from_pdf
from .txt_extractor import extract_text_from_txt
from .docx_extractor import extract_text_from_docx
from .pptx_extractor import extract_text_from_pptx
from .xlsx_extractor import extract_text_from_xlsx
from .djvu_extractor import extract_text_from_djvu
from .image_extractor import extract_text_from_image

def get_file_extractor():
    return {
        ".pdf": extract_text_from_pdf,
        ".txt": extract_text_from_txt,
        ".docx": extract_text_from_docx,
        ".pptx": extract_text_from_pptx,
        ".xlsx": extract_text_from_xlsx,
        ".djvu": extract_text_from_djvu,
        ".jpg": extract_text_from_image,
        ".jpeg": extract_text_from_image,
        ".png": extract_text_from_image,
        ".html": extract_text_common,
        ".md": extract_text_common,
        ".csv": extract_text_common
    }