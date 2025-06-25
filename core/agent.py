from core.command_router import route_command
from utils.helpers import clean_text, contains_exit_command
from utils.constants import EXIT_COMMANDS
from llm.emotion_classifier import classify_emotion
from output.text_output import print_response
from output.speech_output import speak

def process_input(user_text: str) -> bool:
    cleaned = clean_text(user_text)

    # Проверка на выход
    if contains_exit_command(cleaned, EXIT_COMMANDS):
        speak("До встречи!")
        print("🚪 Завершение работы по команде пользователя.")
        return False

    # Эмоциональный анализ (в будущем можно адаптировать стиль)
    emotion = classify_emotion(cleaned)
    print(f"🧠 Обнаружена эмоция: {emotion}")

    # Получить ответ (из базы, LLM или действия)
    response = route_command(cleaned)

    # Ответ пользователю
    speak(response)
    print_response(response)

    return True
