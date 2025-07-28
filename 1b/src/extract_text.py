import pdfplumber
from src.utils import clean_text

def extract_pdf_sections(pdf_path):
    """Extract text from each page in a PDF."""
    section_map = {}
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            text = page.extract_text() or ''
            section_map[i + 1] = clean_text(text)
    return section_map
