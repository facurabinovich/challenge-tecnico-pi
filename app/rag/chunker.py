from docx import Document


def chunk_by_paragraph(doc_path: str) -> list[str]:
    """
    Divide el documento en chunks por párrafos.
    Se eliminan los párrafos vacíos o que solo contienen espacios.
    """
    doc = Document(doc_path)
    chunks = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
    return chunks