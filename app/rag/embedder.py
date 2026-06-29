from dotenv import load_dotenv
import voyageai
from app import config

load_dotenv()

voyage_client = voyageai.Client()

def generate_embedding(chunks, model=config.VOYAGE_MODEL, input_type="document"):
    """
    Genera embeddings para uno o varios textos.
    input_type="document" para indexar, "query" para buscar.
    """
    is_list = isinstance(chunks, list)
    texts = chunks if is_list else [chunks]
    result = voyage_client.embed(texts, model=model, input_type=input_type)
    return result.embeddings if is_list else result.embeddings[0]

