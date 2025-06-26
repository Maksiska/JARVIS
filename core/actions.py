import os
import subprocess
import webbrowser

def _find_chrome() -> str | None:
    """Try to locate Chrome in standard Windows locations."""
    possible = [
        os.path.join(os.environ.get("PROGRAMFILES", "C:\\Program Files"),
                     "Google", "Chrome", "Application", "chrome.exe"),
        os.path.join(os.environ.get("PROGRAMFILES(X86)", "C:\\Program Files (x86)"),
                     "Google", "Chrome", "Application", "chrome.exe"),
        os.path.join(os.environ.get("LOCALAPPDATA", os.path.expanduser("~\\AppData\\Local")),
                     "Google", "Chrome", "Application", "chrome.exe"),
    ]
    for path in possible:
        if os.path.exists(path):
            return path
    return None

# Программы (пути можно дополнить под свою систему)
_CHROME = _find_chrome() or "chrome"

APP_PATHS = {
    "telegram": "C:\\Users\\rm240\\AppData\\Roaming\\Telegram Desktop\\Telegram.exe",
    "discord": "C:\\Path\\Discord.exe",
    "chrome": _CHROME,
    "browser": _CHROME,
}

# Известные папки
KNOWN_FOLDERS = {
    "downloads": "C:\\Users\\rm240\\Downloads",
    "desktop": "C:\\Users\\rm240\\Desktop",
    "documents": "C:\\Users\\rm240\\Documents"
}

def execute_action(action_type: str, action_target: str) -> tuple[bool, str]:
    """Execute action and report success."""
    try:
        if action_type == "launch_app":
            app_name = action_target.lower()
            target = APP_PATHS.get(app_name)

            if target:
                try:
                    subprocess.Popen(target)
                    return True, f"Запускаю {action_target}."
                except Exception:
                    pass  # попробуем резервный способ

            if app_name in ("browser", "chrome"):
                try:
                    webbrowser.get().open("")
                    return True, "Запускаю браузер."
                except Exception:
                    return False, "Не удалось найти путь до браузера."

            return False, f"Не знаю путь для программы '{action_target}'."

        elif action_type == "open_url":
            webbrowser.open(action_target)
            return True, f"Открываю сайт {action_target}."

        elif action_type == "open_folder":
            folder_name = action_target.lower()
            if folder_name in KNOWN_FOLDERS:
                os.startfile(KNOWN_FOLDERS[folder_name])
                return True, f"Открываю папку {action_target}."
            else:
                return False, f"Не знаю путь для папки '{action_target}'."

        elif action_type == "open_path":
            if os.path.exists(action_target):
                if os.path.isdir(action_target):
                    subprocess.run(f'explorer "{action_target}"')
                else:
                    subprocess.run(f'explorer /select,"{action_target}"')
                return True, f"Открываю {action_target}."
            else:
                return False, f"⚠️ Путь {action_target} больше не существует."

        else:
            return False, "Неизвестный тип действия."

    except Exception as e:
        return False, f"Ошибка при выполнении действия: {e}"
