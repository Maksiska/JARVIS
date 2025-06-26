from input.vad import listen_full_phrase
from core.agent import process_input
from core.memory import load_from_file, save_to_file

def main():
    print("🧠 Jarvis Assistant запущен.")
    load_from_file()

    try:
        while True:
            command_text = listen_full_phrase()

            if command_text:
                keep_running = process_input(command_text)
                if not keep_running:
                    break
            else:
                print("Ожидаю новую команду...")

    except KeyboardInterrupt:
        print("\n🛑 Принудительное завершение.")
    finally:
        save_to_file()
        print("💾 История сохранена. Пока!")

if __name__ == "__main__":
    main()
