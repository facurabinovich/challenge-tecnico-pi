from app import config
from dotenv import load_dotenv
from anthropic import Anthropic
from app.rag.retriever import buscar_chunks

load_dotenv()

client = Anthropic()

def run_pipeline(query: str, usuario: str) -> str:

    chunks_encontrados = buscar_chunks(query, n_results=2)
    contexto = "\n\n".join(chunks_encontrados)# "\n\n" hace que cada chunk esté separado por una línea en blanco, para que el modelo pueda distinguirlos mejor.

    system_prompt  = """
            Sos el manager literario de un autor y conoces de que se trata cada una de sus historias. 
            Responder las preguntas con precisión basándote ÚNICAMENTE en el contexto provisto.
    <constraints>
        - Ante la misma pregunta siempre responder exactamente igual
        - Responder en UNA SOLA oración
        - CRITICAL: Detectar el idioma de la "Pregunta" del usuario e ignorar el idioma del contexto. Responder SIEMPRE en el idioma de la pregunta. Pregunta en inglés → responder en inglés. Pregunta en español → responder en español.
        - Agregar emojis que resumen el contenido de la respuesta
        - Responder en 3ra persona
    </constraints>
    """

    messages = [
        {
            "role": "user",
            "content": f"[CONTEXTO]\n{contexto}\n\n[PREGUNTA - responder en el idioma de esta pregunta]: {query}"
        }
    ]

    respuesta = client.messages.create(
        model=config.MODEL, 
        max_tokens=300,
        system=system_prompt,
        messages=messages,
        temperature=0
    )

    return respuesta.content[0].text