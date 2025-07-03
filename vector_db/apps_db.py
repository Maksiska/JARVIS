from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain.schema.document import Document
from core import config
from core.semantic_cleaner import semantic_clean_via_llm
from llm.ollama_client import ask_llm
from utils.helpers import extract_json_from_text

embedding = OllamaEmbeddings(model=config.OLLAMA_MODEL)

apps_db = Chroma(
    collection_name="apps_commands",
    persist_directory="chromadb_apps",
    embedding_function=embedding
)

def add_app_command(command_text: str, action_type: str, action_target: str):
    cleaned = semantic_clean_via_llm(command_text)
    if search_command(cleaned, threshold=0.95):
        print(f"⚠️ Похожая команда уже есть в базе: {cleaned}")
        return

    doc = Document(
        page_content=cleaned,
        metadata={
            "action_type": action_type,
            "action_target": action_target
        }
    )
    apps_db.add_documents([doc])
    apps_db.persist()
    print(f"✅ Команда сохранена: '{cleaned}' → {action_target}")

def search_command(user_input: str, threshold=0.8, k=1) -> dict | None:
    cleaned = semantic_clean_via_llm(user_input)
    results = apps_db.similarity_search_with_relevance_scores(cleaned, k=k)
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
    Определи действие пользователя и верни результат строго в формате JSON.

    Jarvis запускает приложения следующим образом:
    - для встроенных программ Windows указывай их короткое имя (например: notepad, calc);
    - для сторонних программ указывай название. Jarvis будет искать файл "<название>.exe" и запускать его (пример: telegram.exe).
    - перед выбором действия просматривай что тебе пришло, если ты знаешь что есть такое приложение то ставь "launch_app" и возвращай название этого приложения, остальное смотри по промту,
      елси пришла фраза в которой есть фраза "открой файл", то ставь метку "search_files", а если "открой папку", то соответственно "open_folder" и так далее, ниже приведены инструкции

    Возможные действия:
    - "launch_app" — запуск программы
    - "open_url" — открыть сайт
    - "open_folder" — открыть стандартную папку
    - "search_files" — открыть файл
    - "console" - консольные команды
    - "unknown" — если действие определить нельзя

    Формат ответа строго JSON:
    {
        "action_type": "...",
        "action_target": "..."
    }

    Никаких пояснений. Только JSON.

    Примеры:

    Вход: "открой блокнот" или "открой калькулятор"
    Ответ: {"action_type": "console", "action_target": "notepad"}

    Вход: "открой браузер"
    Ответ: {"action_type": "console", "action_target": "browser", "console_command": "start chrome"}

    Вход: "открой сайт ютуб"
    Ответ: {"action_type": "open_url", "action_target": "https://youtube.com", "console_command": "start https://youtube.com"}

    Вход: "открой файл новый текстовый документ"
    Ответ: {"action_type": "search_files", "action_target": "новый текстовый документ", "console_command": ""}

    Вход: "открой папку AI"
    Ответ: {"action_type": "open_folder", "action_target": "AI", "console_command": ""}

    Вход: "выключи компьютер"
    Ответ: {"action_type": "console", "action_target": "", "console_command": "shutdown /s /t 3"}

    Вход: "прочитай анекдот"
    Ответ: {"action_type": "unknown", "action_target": "", "console_command": ""}

    Вход: "открой приложение telegram"
    Ответ: {"action_type": "launch_app", "action_target": "telegram", "console_command": ""}

    Вход: "запусти CapCut"
    Ответ: {"action_type": "launch_app", "action_target": "CapCut", "console_command": ""}
    """

    full_prompt = f"{system_prompt}\n\nВход: \"{user_input}\"\nОтвет:"

    llm_response = ask_llm(full_prompt)
    print("[DEBUG] Ответ LLM:", llm_response)

    parsed = extract_json_from_text(llm_response)
    if parsed is not None:
        return parsed
    print(f"❌ Ошибка парсинга JSON")
    return {"action_type": "unknown", "action_target": ""}