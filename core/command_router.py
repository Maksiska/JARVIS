from vector_db.apps_db import search_command, add_app_command, ask_llm_action_classify
from core.actions import execute_action
from llm.ollama_client import ask_llm
from llm.action_interpreter import interpret_action
from vector_db.similarity_search import get_or_create_response
from core.path_search import search_paths_interactive, ask_user_choose_path
import os

def route_command(command_text: str) -> str:
    # === Переобучение пути ===
    if command_text.lower().startswith(("переобучи", "обнови", "измени путь")):
        target_name = command_text.split(maxsplit=1)[1] if len(command_text.split()) > 1 else ""
        if not target_name:
            return "Что нужно переобучить? Назовите папку."

        paths_found = search_paths_interactive(target_name)
        if paths_found:
            for path in paths_found:
                add_app_command(target_name, "open_path", path)

            if len(paths_found) == 1:
                return execute_action("open_path", paths_found[0])
            else:
                chosen = ask_user_choose_path(paths_found)
                if chosen:
                    return execute_action("open_path", chosen)
                else:
                    return "Выбор отменён."
        else:
            return "Ничего не найдено для обновления."

    # === Команда "открой папку ..."
    if command_text.lower().startswith("открой папку"):
        folder_name = command_text.split("открой папку", 1)[1].strip()

        result = search_command(folder_name)
        if result:
            print(f"[DEBUG] Найдено в apps_db: {result}")
            path = result["action_target"]
            if os.path.exists(path):
                return execute_action("open_path", path)
            else:
                return "⚠️ Путь не существует. Скажи: 'переобучи название' чтобы обновить."

        print("Запускаю поиск по дискам...")
        paths_found = search_paths_interactive(folder_name)
        if paths_found:
            for path in paths_found:
                add_app_command(folder_name, "open_path", path)

            if len(paths_found) == 1:
                return execute_action("open_path", paths_found[0])
            else:
                chosen = ask_user_choose_path(paths_found)
                if chosen:
                    return execute_action("open_path", chosen)
                else:
                    return "Выбор отменён."
        else:
            return "Ничего не найдено."

    # === Поиск в apps_db (твоя логика)
    result = search_command(command_text)
    if result:
        print(f"[DEBUG] Найдено в apps_db: {result}")

        if result["action_type"] == "open_path":
            path = result["action_target"]
            if os.path.exists(path):
                return execute_action("open_path", path)
            else:
                return "⚠️ Путь не существует. Скажи: 'переобучи название' чтобы обновить."
        else:
            return execute_action(result["action_type"], result["action_target"])

    # === Поиск в ChromaDB → LLM → обучение
    print("🔍 Поиск в ChromaDB...")
    action = get_or_create_response(command_text, interpret_action)

    if action["action_type"] != "unknown":
        if action["action_type"] != "search_files":
            add_app_command(command_text, action["action_type"], action["action_target"])
        return execute_action(action["action_type"], action["action_target"])

    # === Если LLM не поняла → короткий ответ
    print("LLM не распознала команду → отвечаю коротко")
    short_prompt = f"Отвечай коротко, для голосового ассистента: {command_text}"
    return ask_llm(short_prompt)
