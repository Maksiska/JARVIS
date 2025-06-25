from input.vad import wait_for_wake_word, listen_command
from input.transcription import transcribe_audio
from core.agent import process_input
from core.memory import load_from_file, save_to_file
from utils.helpers import debug_log

def main():
    print("🧠 Jarvis Assistant запущен.")
    load_from_file()

    try:
        while True:
            if wait_for_wake_word():
                audio = listen_command()
                if not audio:
                    continue

                text = transcribe_audio(audio)
                if not text.strip():
                    print("🤷 Пустой запрос. Повторите.")
                    continue

                debug_log(f"📥 Получено: {text}")
                keep_running = process_input(text)

                if not keep_running:
                    break

    except KeyboardInterrupt:
        print("\n🛑 Принудительное завершение работы.")
    finally:
        save_to_file()
        print("💾 История сохранена. Пока!")

if __name__ == "__main__":
    main()
