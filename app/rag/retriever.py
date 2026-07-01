import chromadb
from app import config
from app.rag.embedder import generate_embedding

chroma_client = chromadb.PersistentClient(path=config.CHROMA_PATH)

def _get_collection():
    return chroma_client.get_or_create_collection(name=config.COLLECTION_NAME)

def indexar_documento(chunks: list[str]) -> None:
    """
    Genera embeddings para todos los chunks y los carga en ChromaDB.
    Pisa la colección si ya existía para evitar duplicados.
    """
    try:
        chroma_client.delete_collection(name=config.COLLECTION_NAME)
    except Exception:
        pass

    collection = _get_collection()
    embeddings = generate_embedding(chunks, input_type="document")

    for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)): # enumerate (zip) para obtener el índice y el chunk al mismo tiempo
        collection.add(
            ids=[f"chunk_{i}"],
            embeddings=[embedding],
            documents=[chunk],
        )

    print(f"Indexados {len(chunks)} chunks en '{config.COLLECTION_NAME}'.")


def buscar_chunks(query: str, n_results: int = 2) -> list[str]:
    """
    Embeds la query y devuelve los n chunks más relevantes.
    """
    collection = _get_collection()
    query_embedding = generate_embedding(query, input_type="query")
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results,
    )
    return results["documents"][0]  
# [0] porque query() devuelve una lista de listas (una por cada query enviada); como siempre enviamos
#  una sola query, tomamos el primer elemento.
# Si haces collection.query con n_results=2, results["documents"] luce así:
# 
# [                                          ← lista exterior (una entrada por query enviada)
#     ["Zara es una exploradora...",         ← lista interior: los 2 chunks más relevantes
#      "En la galaxia de Zenthoria..."]
# ]
#
# results["documents"][0]  →  ["Zara es una exploradora...", "En la galaxia de Zenthoria..."]
# results["documents"][0][0]  →  "Zara es una exploradora..."
# results["documents"][0][1]  →  "En la galaxia de Zenthoria..."