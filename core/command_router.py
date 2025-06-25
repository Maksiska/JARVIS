from utils.constants import SUPPORTED_ACTIONS
from utils.helpers import extract_keywords
from core.actions import try_execute_action
from vector_db.similarity_search import get_or_create_response
from llm.ollama_client import ask_llm

def route_command(command_text: str) -> str:
    # 1. Проверяем, не является ли команда действием
    keywords = extract_keywords(command_text, SUPPORTED_ACTIONS)
    if keywords:
        return try_execute_action(command_text)

    # 2. Если это не действие — ищем похожую команду или вызываем LLM
    response = get_or_create_response(command_text, ask_llm)
    return response
