import speech_recognition as sr
from input.transcription import transcribe_audio

recognizer = sr.Recognizer()

def wait_for_wake_word(wake_word="джарвис", timeout=3, phrase_time_limit=3) -> bool:
    """
    Слушает короткие фрагменты и активируется при обнаружении ключевого слова.
    """
    print("🔎 Ожидаю активационное слово 'Jarvis'...")
    recognizer.energy_threshold = 300
    recognizer.pause_threshold = 1.0

    while True:
        try:
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source, duration=1)
                audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
                text = transcribe_audio(audio).lower()
                print(f"📥 Услышано: {text}")
                if wake_word.lower() in text:
                    print("✅ Обнаружено имя 'Jarvis'. Готов к команде.")
                    return True
        except sr.WaitTimeoutError:
            print("⌛ Нет речи. Повторная попытка.")
        except Exception as e:
            print(f"❌ Ошибка при прослушивании: {e}")
            continue

def listen_command(timeout=8, pause_threshold=1.2, phrase_time_limit=None):
    """
    Слушает полноценную фразу после активации.
    """
    recognizer.pause_threshold = pause_threshold
    recognizer.energy_threshold = 300

    try:
        with sr.Microphone() as source:
            print("🎤 Слушаю команду...")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            print("✅ Команда записана.")
            return audio
    except sr.WaitTimeoutError:
        print("⌛ Никто не говорит. Пропуск.")
        return None
    except Exception as e:
        print(f"❌ Ошибка при записи команды: {e}")
        return None

