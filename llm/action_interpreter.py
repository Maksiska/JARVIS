from llm.ollama_client import ask_llm
import json

EXAMPLES = """
Вход: "открой браузер"
Ответ: {"action_type": "launch_app", "action_target": "browser", "console_command": "start chrome"}

Вход: "открой сайт ютуб"
Ответ: {"action_type": "open_url", "action_target": "https://youtube.com", "console_command": "start https://youtube.com"}

Вход: "открой папку D:\\Projects\\AI"
Ответ: {"action_type": "open_folder", "action_target": "D:\\Projects\\AI", "console_command": "start D:\\Projects\\AI"}

Вход: "выключи компьютер"
Ответ: {"action_type": "shutdown", "action_target": "", "console_command": "shutdown /s /t 3"}

Вход: "прочитай анекдот"
Ответ: {"action_type": "unknown", "action_target": "", "console_command": ""}
"""

def interpret_action(user_text: str) -> dict:
    prompt = f"""
Ты — интеллектуальный интерпретатор команд пользователя.

Для команды пользователя верни результат в формате JSON:

{{
  "action_type": "...",
  "action_target": "...",
  "console_command": "..."
}}

Где:
- action_type — тип действия (например: "launch_app", "open_folder", "open_url", "shutdown", "unknown")
- action_target — цель (например: "browser", "Downloads", "https://youtube.com")
- console_command — фактическая консольная команда, которая будет выполнена (например: "start chrome", "start D:\\Projects\\AI", "shutdown /s /t 3")

Примеры:

{EXAMPLES}

Теперь обработай:

"{user_text}"

Ответ:
"""

    raw_response = ask_llm(prompt)
    print(f"[DEBUG] Ответ LLM:\n{raw_response}")

    # Попытаемся распарсить JSON
    try:
        parsed = json.loads(raw_response)
        if "action_type" in parsed and "action_target" in parsed and "console_command" in parsed:
            return parsed
        else:
            return {"action_type": "unknown", "action_target": "", "console_command": ""}
    except json.JSONDecodeError:
        print("⚠️ Некорректный JSON от LLM!")
        return {"action_type": "unknown", "action_target": "", "console_command": ""}
