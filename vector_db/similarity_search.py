from vector_db.cromadb_interface import (
    add_command,
    search_similar_command
)
from utils.constants import VECTOR_SEARCH_THRESHOLD
from utils.helpers import debug_log

def get_or_create_response(query: str, generate_response_fn, threshold: float = VECTOR_SEARCH_THRESHOLD) -> tuple[dict, bool]:
    debug_log(f"🔍 Ищем похожую команду: {query}")
    existing = search_similar_command(query, threshold=threshold)

    if existing:
        debug_log("✅ Найдено в базе Chroma.")
        return existing, False

    debug_log("📡 Не найдено. Получаем ответ от LLM...")
    action_dict = generate_response_fn(query)

    return action_dict, True