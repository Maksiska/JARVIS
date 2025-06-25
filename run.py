import subprocess
import time
import os

def launch_llama_model(model="llama3.1:latest"):
    if os.getenv("USE_OLLAMA_HTTP", "false").lower() == "true":
        return

    try:
        print(f"🚀 Запускаем модель LLM: {model}")
        subprocess.Popen(["ollama", "run", model], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(2)
    except Exception as e:
        print(f"❌ Не удалось запустить модель: {e}")

if __name__ == "__main__":
    from app.main import main
    from dotenv import load_dotenv

    load_dotenv()
    launch_llama_model()
    main()
