import re
from pathlib import Path

import fitz
from docx import Document


def normalize_text(text: str) -> str:
    if not text:
        return ''
    text = text.replace('\r', '\n')
    text = re.sub(r'\n+', ' ', text)
    text = re.sub(r'\s{2,}', ' ', text)
    return text.strip()


def extract_text_from_pdf(file_path: str) -> str:
    doc = fitz.open(file_path)
    pages = []
    for page in doc:
        pages.append(page.get_text())
    doc.close()
    return normalize_text('\n'.join(pages))


def extract_text_from_docx(file_path: str) -> str:
    document = Document(file_path)
    paragraphs = [p.text for p in document.paragraphs if p.text.strip()]
    return normalize_text(' '.join(paragraphs))


def extract_text_from_file(file_path: str, extension: str) -> str:
    path = Path(file_path)
    if extension.lower() == '.pdf':
        return extract_text_from_pdf(str(path))
    if extension.lower() == '.docx':
        return extract_text_from_docx(str(path))
    raise ValueError('Unsupported file format')
