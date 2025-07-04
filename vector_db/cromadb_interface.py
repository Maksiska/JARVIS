import os
from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain.schema.document import Document
from core.semantic_cleaner import semantic_clean_via_llm

load_dotenv()

CHROMA_COLLECTION_NAME = os.getenv("CHROMA_COLLECTION_NAME", "commands")
CHROMA_PERSIST_DIR = os.getenv("CHROMA_PERSIST_DIR", "chromadb")

embedding = OllamaEmbeddings(model=os.getenv("OLLAMA_MODEL", "llama3.1:latest"))

db = Chroma(
    collection_name=CHROMA_COLLECTION_NAME,
    persist_directory=CHROMA_PERSIST_DIR,
    embedding_function=embedding
)

def add_command(text: str, action_dict: dict):
    cleaned = semantic_clean_via_llm(text)
    if search_similar_command(cleaned, threshold=0.95):
        print(f"⚠️ Похожая команда уже есть в базе: {cleaned}")
        return

    metadata = {
        "action_type": action_dict.get("action_type", "unknown"),
        "action_target": action_dict.get("action_target", ""),
        "console_command": action_dict.get("console_command", "")
    }
    doc = Document(page_content=cleaned, metadata=metadata)
    db.add_documents([doc])
    db.persist()
    print(f"✅ Добавлено в БД: '{cleaned}' → {metadata}")

def search_similar_command(query: str, k: int = 1, threshold: float = 0.8) -> dict | None:
    cleaned = semantic_clean_via_llm(query)
    results = db.similarity_search_with_relevance_scores(cleaned, k=k)
    if not results:
        return None
    doc, score = results[0]
    if score >= threshold:
        return {
            "action_type": doc.metadata.get("action_type", "unknown"),
            "action_target": doc.metadata.get("action_target", ""),
            "console_command": doc.metadata.get("console_command", "")
        }
    return None
