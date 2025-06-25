from email.message import EmailMessage
import os
import shutil
import smtplib
import subprocess
import webbrowser
import ctypes

import pyautogui
from utils.helpers import debug_log
from output.speech_output import speak

try:
    import pyperclip
except ImportError:
    pyperclip = None

try:
    import PyPDF2
except ImportError:
    PyPDF2 = None

def try_execute_action(command_text: str) -> str:
    text = command_text.lower()

    # === 1. Открытие сайта
    if "сайт" in text:
        url = extract_url(text)
        if url:
            webbrowser.open(url)
            return f"Открываю сайт: {url}"

    # === 2. Браузер
    elif "браузер" in text:
        subprocess.Popen("start chrome", shell=True)
        return "Открываю браузер."

    # === 3. Блокнот
    elif "блокнот" in text:
        subprocess.Popen("notepad", shell=True)
        return "Открываю блокнот."

    # === 4. Папка
    elif "открой папку" in text:
        path = extract_path(text)
        if path and os.path.exists(path):
            os.startfile(path)
            return f"Открываю папку: {path}"
        return "Папка не найдена."

    # === 5. Создание папки
    elif "создай папку" in text:
        path = extract_path(text)
        if path:
            os.makedirs(path, exist_ok=True)
            return f"Папка создана: {path}"

    # === 6. Создание файла
    elif "создай файл" in text:
        path = extract_path(text)
        if path:
            with open(path, "w", encoding="utf-8") as f:
                f.write("")
            return f"Файл создан: {path}"

    # === 7. Удаление
    elif "удали" in text:
        path = extract_path(text)
        if path and os.path.exists(path):
            try:
                if os.path.isfile(path):
                    os.remove(path)
                else:
                    shutil.rmtree(path)
                return f"Удалено: {path}"
            except Exception as e:
                return f"Ошибка при удалении: {e}"
        return "Не найден файл или папка для удаления."

    # === 8. Выключение и перезагрузка
    elif "выключи компьютер" in text:
        subprocess.call("shutdown /s /t 3", shell=True)
        return "Выключаю компьютер..."

    elif "перезагрузи компьютер" in text:
        subprocess.call("shutdown /r /t 3", shell=True)
        return "Перезагружаюсь..."

    # === 9. Блокировка экрана
    elif "заблокируй экран" in text or "заблокируй компьютер" in text:
        ctypes.windll.user32.LockWorkStation()
        return "Экран заблокирован."

    # === 10. Очистка корзины
    elif "очисти корзину" in text:
        try:
            subprocess.call('PowerShell.exe -Command "Clear-RecycleBin -Force"', shell=True)
            return "Корзина очищена."
        except Exception as e:
            return f"Ошибка очистки корзины: {e}"

    # === 11. Чтение файла
    elif "прочти файл" in text:
        path = extract_path(text)
        if path and os.path.isfile(path):
            return read_file_contents(path)
        return "Файл не найден или путь некорректен."
    
    # === 12. Запуск программы по имени
    elif "запусти" in text or "открой программу" in text:
        app_name = extract_app_name(text)
        if app_name:
            return launch_app(app_name)
        return "Не смог определить, какую программу запустить."

    # === 13. Скриншот экрана
    elif "сделай скриншот" in text or "снимок экрана" in text:
        return take_screenshot()

    # === 14. Отправка письма
    elif "отправь письмо" in text or "email" in text:
        return send_email(
            subject="Автоматическое письмо от Jarvis",
            body="Привет! Это тестовое сообщение от твоего ассистента.",
            to="example@example.com"  # замените на нужный email
        )

    return "Команда распознана, но действие не реализовано."

# === Вспомогательные функции ===

def extract_url(text: str) -> str | None:
    for word in text.split():
        if "http" in word:
            return word
    return None

def extract_path(text: str) -> str | None:
    for word in text.split():
        if ":" in word or "\\" in word or "/" in word:
            return word.replace('"', '').strip()
    return None

def read_file_contents(path: str) -> str:
    try:
        if path.endswith(".txt"):
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
                speak(content[:500])  # читаем только начало
                return "Читаю содержимое файла."
        elif path.endswith(".pdf") and PyPDF2:
            with open(path, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                text = ""
                for page in reader.pages[:3]:  # читаем первые 3 страницы
                    text += page.extract_text()
                speak(text[:500])
                return "Читаю содержимое PDF файла."
        else:
            return "Формат файла не поддерживается."
    except Exception as e:
        return f"Ошибка при чтении файла: {e}"

def extract_app_name(text: str) -> str | None:
    words = text.split()
    for i, word in enumerate(words):
        if word in ["запусти", "открой"] and i + 1 < len(words):
            return words[i + 1]
    return None

def launch_app(app: str) -> str:
    app_paths = {
        "telegram": "C:\\Users\\Имя\\AppData\\Roaming\\Telegram Desktop\\Telegram.exe",
        "discord": "C:\\Users\\Имя\\AppData\\Local\\Discord\\Update.exe",
        "калькулятор": "calc",
        "блокнот": "notepad",
        "paint": "mspaint",
        "проводник": "explorer"
    }

    app = app.lower()
    if app in app_paths:
        try:
            subprocess.Popen(app_paths[app], shell=True)
            return f"Запускаю {app}."
        except Exception as e:
            return f"Ошибка при запуске {app}: {e}"
    return "Неизвестное приложение."

def take_screenshot() -> str:
    try:
        path = os.path.join(os.getcwd(), "screenshot.png")
        screenshot = pyautogui.screenshot()
        screenshot.save(path)
        return f"Скриншот сохранён: {path}"
    except Exception as e:
        return f"Ошибка при создании скриншота: {e}"

def send_email(subject: str, body: str, to: str) -> str:
    try:
        EMAIL = os.getenv("SMTP_EMAIL")
        PASSWORD = os.getenv("SMTP_PASSWORD")

        if not EMAIL or not PASSWORD:
            return "SMTP-настройки не заданы в .env"

        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = EMAIL
        msg["To"] = to
        msg.set_content(body)

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(EMAIL, PASSWORD)
            smtp.send_message(msg)

        return f"Письмо отправлено на {to}."
    except Exception as e:
        return f"Ошибка при отправке письма: {e}"

