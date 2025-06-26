import os
import string
import subprocess

def get_all_disks():
    disks = []
    for drive in string.ascii_uppercase:
        drive_path = f"{drive}:\\" 
        if os.path.exists(drive_path):
            disks.append(drive_path)
    return disks

def search_exact_folder(target_name):
    found_folders = []
    disks = get_all_disks()
    print(f"Поиск папок: '{target_name}'\n")

    for disk in disks:
        print(f"Идёт поиск на {disk}...")
        for root, dirs, _ in os.walk(disk):
            for dir_name in dirs:
                if dir_name.lower() == target_name.lower():
                    full_path = os.path.join(root, dir_name)
                    found_folders.append(full_path)
    return found_folders

def search_files_any_extension(target_name):
    found_files = []
    disks = get_all_disks()
    print(f"\nПапка не найдена. Ищем файлы: '{target_name}.*'\n")

    for disk in disks:
        print(f"Идёт поиск на {disk}...")
        for root, _, files in os.walk(disk):
            for file_name in files:
                name, _ = os.path.splitext(file_name)
                if name.lower() == target_name.lower():
                    full_path = os.path.join(root, file_name)
                    found_files.append(full_path)
    return found_files

def open_path(path):
    if os.path.isdir(path):
        subprocess.run(f'explorer "{path}"')
    elif os.path.isfile(path):
        subprocess.run(f'explorer /select,"{path}"')

def search_paths_interactive(target_name: str):
    folders = search_exact_folder(target_name)

    if folders:
        print(f"\nНайдено папок: {len(folders)}")
        return folders
    else:
        files = search_files_any_extension(target_name)
        if files:
            print(f"\nНайдено файлов: {len(files)}")
            return files
        else:
            print("\nНичего не найдено.")
            return None

def ask_user_choose_path(paths):
    print("\nНайдено несколько вариантов:")
    for idx, path in enumerate(paths, start=1):
        print(f"{idx}) {path}")

    while True:
        choice = input("\nВыберите номер (или 0 для отмены): ")
        if choice.isdigit():
            choice = int(choice)
            if choice == 0:
                return None
            elif 1 <= choice <= len(paths):
                return paths[choice - 1]
            else:
                print("Некорректный номер.")
        else:
            print("Введите цифру.")
