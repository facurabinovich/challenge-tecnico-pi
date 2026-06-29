from app.rag.chunker import chunk_by_paragraph
from app.rag.retriever import indexar_documento
from app import config
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

raw_chunks = chunk_by_paragraph(config.DOC_PATH)
indexar_documento(raw_chunks)