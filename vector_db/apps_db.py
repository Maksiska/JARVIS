from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain.schema.document import Document
from core import config
import json
from llm.ollama_client import ask_llm

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
    Ты — модуль классификации команд в проекте Jarvis.
    Определи действие пользователя и верни результат в формате JSON.

    Jarvis запускает приложения следующим образом:
    - для встроенных программ Windows указывай их короткое имя (например: notepad, calc);
    - для сторонних программ указывай название. Jarvis будет искать файл "<название>.exe" и запускать его (пример: telegram.exe).

    Возможные действия:
    - "launch_app" — запуск программы
    - "open_url" — открыть сайт
    - "open_folder" — открыть стандартную папку
    - "open_path" — открыть конкретный путь
    - "volume_up" — увеличить громкость
    - "volume_down" — уменьшить громкость
    - "unknown" — если действие определить нельзя

    Формат ответа строго JSON:
    {
        "action_type": "...",
        "action_target": "..."
    }

    Никаких пояснений. Только JSON.

    Примеры:

    Вход: "открой блокнот"
    Ответ: {"action_type": "launch_app", "action_target": "notepad"}

    Вход: "открой телеграм"
    Ответ: {"action_type": "launch_app", "action_target": "telegram"}

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

    try:
        json_start = llm_response.find("{")
        json_str = llm_response[json_start:]
        return json.loads(json_str)
    except Exception as e:
        print(f"❌ Ошибка парсинга JSON: {e}")
        return {"action_type": "unknown", "action_target": ""}
