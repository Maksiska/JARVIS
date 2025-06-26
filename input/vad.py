import speech_recognition as sr
from input.transcription import transcribe_audio

recognizer = sr.Recognizer()

def listen_full_phrase(wake_word="джарвис", timeout=8, pause_threshold=1.2):
    """
    Слушает полную фразу с ключевым словом ('джарвис команда ...')
    """
    recognizer.pause_threshold = pause_threshold
    recognizer.energy_threshold = 300

    with sr.Microphone() as source:
        print("🎤 Слушаю полную фразу...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        try:
            audio = recognizer.listen(source, timeout=timeout)
            print("✅ Фраза записана.")
        except sr.WaitTimeoutError:
            print("⌛ Время ожидания истекло.")
            return None

    # Преобразуем в текст
    text_raw = transcribe_audio(audio)
    if not text_raw:
        print("🤷 Ничего не распознано.")
        return None

    text = text_raw.lower()
    print(f"[DEBUG] Распознано: {text}")

    # Проверяем наличие wake word
    if wake_word in text:
        command = text.split(wake_word, 1)[1].strip()
        print(f"📋 Команда: {command}")
        return command
    else:
        print("❌ Слово 'Jarvis' не услышал.")
        return None
