import os
import subprocess
import webbrowser
from core.path_search import search_applications, ask_user_choose_path, open_path, search_files, search_folder, search_paths_interactive_app

def execute_action(action_type: str, action_target: str) -> str:
    try:
        if action_type == "launch_app":
            search_paths_interactive_app(action_target)
            return f"Запускаю {action_target}"
                    
        elif action_type == "open_url":
            webbrowser.open(action_target)
            return f"Открываю сайт {action_target}."

        elif action_type == "search_files": 
            paths_found = search_files(action_target)
            if paths_found:
                if len(paths_found) == 1:
                    open_path(paths_found[0])
                    return f"Открываю {paths_found[0]}."
                else:
                    chosen = ask_user_choose_path(paths_found)
                    if chosen:
                        open_path(chosen)
                        return f"Открываю {chosen}."
                    else:
                        return "Выбор отменён."
            else:
                return "Ничего не найдено."
            
        elif action_type == "open_folder":
            paths_found = search_folder(action_target)
            if paths_found:
                if len(paths_found) == 1:
                    open_path(paths_found[0])
                    return f"Открываю {paths_found[0]}."
                else:
                    chosen = ask_user_choose_path(paths_found)
                    if chosen:
                        open_path(chosen)
                        return f"Открываю {chosen}."
                    else:
                        return "Выбор отменён."
            else:
                return "Ничего не найдено."

        else:
            return "Неизвестный тип действия."

    except Exception as e:
        return f"Ошибка при выполнении действия: {e}"