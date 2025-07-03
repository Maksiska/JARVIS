from vector_db.apps_db import search_command, add_app_command
from core.actions import execute_action
from llm.ollama_client import ask_llm
from llm.action_interpreter import interpret_action
from vector_db.cromadb_interface import add_command
import os
import subprocess

def route_command(command_text: str) -> str:
    
    result = search_command(command_text)
    if result:
        print(f"[DEBUG] Найдено в apps_db: {result}")
        
        if result["action_type"] == "launch_app":
            msg = execute_action("launch_app", result["action_target"])
            return msg
        
        elif result["action_type"] == "search_files":
            return execute_action("search_files", result["action_target"])
        
        elif result["action_type"] == "open_folder":
            return execute_action("open_folder", result["action_target"])
        
        elif result["action_type"] == "console":
            try:
                subprocess.run(result["action_target"], shell=True)
                return f"✅ Выполняю: {result['action_target']}"
            except Exception as e:
                return f"⚠️ Ошибка выполнения: {e}"
            
        elif result["action_type"] == "open_url":
            return execute_action("open_url", result["action_target"])
        else:
            return execute_action(result["action_type"], result["action_target"])

    action = interpret_action(command_text)

    if action["action_type"] == "search_files":
        name_only = os.path.basename(action["action_target"].strip().rstrip("\/"))
        return execute_action("search_files", name_only)

    elif action["action_type"] == "open_folder":
        name_only = os.path.basename(action["action_target"].strip().rstrip("\/"))
        return execute_action("open_folder", name_only)
    
    elif action["action_type"] == "open_url":
        name_only = os.path.basename(action["action_target"].strip().rstrip("\/"))
        return execute_action("open_url", name_only)
    
    elif action["action_type"] == "launch_app":
        name_only = os.path.basename(action["action_target"].strip().rstrip("\/"))
        return execute_action("launch_app", name_only)

    elif action["action_type"] == "unknown":
        print("LLM не распознала команду → отвечаю коротко")
        return ask_llm(f"Отвечай коротко, для голосового ассистента: {command_text}")

    elif action["console_command"]:
        try:
            subprocess.run(action["console_command"], shell=True)
            add_command(command_text, action)
            return f"✅ Выполняю: {action['console_command']}"
        except Exception as e:
            return f"⚠️ Ошибка выполнения: {e}"

    add_app_command(command_text, action["action_type"], action["action_target"])
    return execute_action(action["action_type"], action["action_target"])
