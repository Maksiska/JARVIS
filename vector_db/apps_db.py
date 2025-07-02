from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain.schema.document import Document
from core import config
import json
from llm.ollama_client import ask_llm
from utils.helpers import extract_json_from_text

embedding = OllamaEmbeddings(model=config.OLLAMA_MODEL)

apps_db = Chroma(
    collection_name="apps_commands",
    persist_directory="chromadb_apps",
    embedding_function=embedding
)

def add_app_command(command_text: str, action_type: str, action_target: str):
    doc = Document(
        page_content=command_text,
        metadata={
            "action_type": action_type,
            "action_target": action_target
        }
    )
    apps_db.add_documents([doc])
    apps_db.persist()
    print(f"✅ Команда сохранена: '{command_text}' → {action_target}")

def search_command(user_input: str, threshold=0.8, k=1) -> dict | None:
    results = apps_db.similarity_search_with_score(user_input, k=k)
    if not results:
        return None
    doc, score = results[0]
    print(f"[DEBUG] Сходство: {score:.2f}")
    if score >= threshold:
        return doc.metadata
    return None

def ask_llm_action_classify(user_input: str) -> dict:
    system_prompt = """
    Ты — помощник для голосового ассистента Jarvis.

    Определи, что делает команда пользователя:
    - "launch_app" — запуск программы (например: Telegram, Chrome, VLC)
    - "open_url" — открыть сайт (URL, например: https://youtube.com)
    - "open_folder" — открыть стандартную папку (Downloads, Documents, Desktop)
    - "open_path" — открыть конкретный путь на диске
    - "volume_up" — увеличить громкость
    - "volume_down" — уменьшить громкость
    - "unknown" — если не удалось определить

    Формат ответа — СТРОГО JSON:
    {
        "action_type": "...",
        "action_target": "..."
    }

    Отвечай КРАТКО. Никаких объяснений, только JSON.

    Примеры:

    Вход: "открой браузер"
    Ответ: {"action_type": "launch_app", "action_target": "browser"}

    Вход: "увеличь громкость"
    Ответ: {"action_type": "volume_up", "action_target": ""}

    Вход: "открой папку загрузки"
    Ответ: {"action_type": "open_folder", "action_target": "Downloads"}

    Вход: "открой сайт ютуб"
    Ответ: {"action_type": "open_url", "action_target": "https://youtube.com"}

    Вход: "открой папку D:\Projects\AI"
    Ответ: {"action_type": "open_path", "action_target": "D:\\Projects\\AI"}

    Вход: "прочитай анекдот"
    Ответ: {"action_type": "unknown", "action_target": ""}
    """

    full_prompt = f"{system_prompt}\n\nВход: \"{user_input}\"\nОтвет:"

    llm_response = ask_llm(full_prompt)
    print("[DEBUG] Ответ LLM:", llm_response)

    parsed = extract_json_from_text(llm_response)
    if parsed is not None:
        return parsed
    print(f"❌ Ошибка парсинга JSON")
    return {"action_type": "unknown", "action_target": ""}
