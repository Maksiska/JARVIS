import os
from dotenv import load_dotenv
from langchain.embeddings import OllamaEmbeddings

load_dotenv()

OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.1:latest")

# Инициализация эмбеддингов от Ollama
embedding_model = OllamaEmbeddings(model=OLLAMA_MODEL)

def get_text_embedding(text: str) -> list:
    try:
        return embedding_model.embed_query(text)
    except Exception as e:
        print(f"❌ Ошибка при генерации эмбеддинга: {e}")
        return []
