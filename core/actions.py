import os
import subprocess
import webbrowser

# Программы (пути можно дополнить под свою систему)
APP_PATHS = {
    "telegram": "C:\\Users\\rm240\\AppData\\Roaming\\Telegram Desktop\\Telegram.exe",
    "discord": "C:\\Path\\Discord.exe",
    "chrome": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
}

# Известные папки
KNOWN_FOLDERS = {
    "downloads": "C:\\Users\\rm240\\Downloads",
    "desktop": "C:\\Users\\rm240\\Desktop",
    "documents": "C:\\Users\\rm240\\Documents"
}

def execute_action(action_type: str, action_target: str) -> str:
    try:
        if action_type == "launch_app":
            app_name = action_target.lower()
            if app_name in APP_PATHS:
                subprocess.Popen(APP_PATHS[app_name])
                return f"Запускаю {action_target}."
            else:
                return f"Не знаю путь для программы '{action_target}'."

        elif action_type == "open_url":
            webbrowser.open(action_target)
            return f"Открываю сайт {action_target}."

        elif action_type == "open_folder":
            folder_name = action_target.lower()
            if folder_name in KNOWN_FOLDERS:
                os.startfile(KNOWN_FOLDERS[folder_name])
                return f"Открываю папку {action_target}."
            else:
                return f"Не знаю путь для папки '{action_target}'."

        elif action_type == "open_path":
            if os.path.exists(action_target):
                if os.path.isdir(action_target):
                    subprocess.run(f'explorer "{action_target}"')
                else:
                    subprocess.run(f'explorer /select,"{action_target}"')
                return f"Открываю {action_target}."
            else:
                return f"⚠️ Путь {action_target} больше не существует."

        else:
            return "Неизвестный тип действия."

    except Exception as e:
        return f"Ошибка при выполнении действия: {e}"
