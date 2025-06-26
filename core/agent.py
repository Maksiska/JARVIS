from core.command_router import route_command
from core.semantic_cleaner import semantic_clean_via_llm
from utils.helpers import clean_text, contains_exit_command
from utils.constants import EXIT_COMMANDS
from llm.emotion_classifier import classify_emotion
from output.text_output import print_response
from output.speech_output import speak
from core.memory import add_message

def process_input(user_text: str) -> bool:
    """
    Обрабатывает входной текст:
    - проверяет на команду выхода
    - определяет эмоцию
    - получает ответ от route_command
    - озвучивает и выводит результат
    """

    cleaned = clean_text(user_text)

    if not cleaned.strip():
        print("🤷 Я не понял, что вы сказали.")
        return True  # продолжаем цикл

    # Проверка на выход
    if contains_exit_command(cleaned, EXIT_COMMANDS):
        speak("До встречи!")
        print("🚪 Завершаю работу.")
        return False  # выход из цикла

    # Эмоции
    emotion = classify_emotion(cleaned)
    print(f"🧠 Обнаружена эмоция: {emotion}")

    # Запоминаем вход
    add_message(role="user", content=cleaned)

    semantic = semantic_clean_via_llm(cleaned)
    print(f"🧹 Очищено для поиска: {semantic}")

    # Пускаем дальше
    response = route_command(semantic)

    # Запоминаем ответ
    add_message(role="bot", content=response)

    # Озвучиваем
    speak(response)
    print_response(response)

    return True
