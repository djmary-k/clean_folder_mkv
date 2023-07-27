# У clean_folder/clean_folder/clean.py потрібно помістити все, що ми зробили у попередніх домашніх завданнях 
# по розбору папки. Ваше основне завдання написати clean_folder/setup.py, щоб вбудований інструментарій 
# Python міг встановити цей пакет та операційна система могла використати цей пакет як консольну команду.
# Критерії приймання завдання
# Пакет встановлюється в систему командою pip install -e . (або python setup.py install, потрібні права адміністратора).
# Після встановлення в системі з'являється пакет clean_folder.
# Коли пакет встановлений в системі, скрипт можна викликати у будь-якому місці з консолі командою clean-folder
# Консольний скрипт обробляє аргументи командного рядка точно так, як і Python-скрипт.

import re
import sys
from pathlib import Path
import shutil
# import sort as parser # sort - rename
# from normalize import normalize

# translation part
CYRILLIC_SYMBOLS = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ'
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "u", "ja", "je", "ji", "g")
TRANS = {}
for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    TRANS[ord(c)] = l
    TRANS[ord(c.upper())] = l.upper()

# normalize names of files
def normalize(name: str) -> str:
    t_name = name.translate(TRANS)
    t_name = re.sub(r'[^a-zA-Z0-9.]', '_', t_name) 
    return t_name


# sort part
# def parser():
    
# images ('JPEG', 'PNG', 'JPG', 'SVG')
IMAGES = []
# video ('AVI', 'MP4', 'MOV', 'MKV')
VIDEO = []
# documents ('DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX')
DOCS = []
# audio ('MP3', 'OGG', 'WAV', 'AMR')
AUDIO = []
# archives ('ZIP', 'GZ', 'TAR')
ARCHIVES = []
# other files
OTHERS = []

REGISTER_EXTENSION = {
    'JPEG': IMAGES,
    'JPG': IMAGES,
    'PNG': IMAGES,
    'SVG': IMAGES,
    'AVI': VIDEO,
    'MP4': VIDEO,
    'MOV': VIDEO,
    'MKV': VIDEO,
    'DOC': DOCS,
    'DOCX': DOCS,
    'TXT': DOCS,
    'PDF': DOCS,
    'XLSX': DOCS,
    'PPTX': DOCS,
    'MP3': AUDIO,
    'OGG': AUDIO,
    'WAV': AUDIO,
    'AMR': AUDIO,
    'ZIP': ARCHIVES,
    'GZ': ARCHIVES,
    'TAR': ARCHIVES
}

FOLDERS = []
EXTENSION = set()
UNKNOWN = set()

def get_extension(filename: str) -> str:
    return Path(filename).suffix[1:].upper()  # перетворюємо розширення файлу на назву папки jpg -> JPG

def scan(folder: Path) -> None:
    for item in folder.iterdir():
        # Якщо це папка то додаємо її до списку FOLDERS і переходимо до наступного елемента папки
        if item.is_dir():
            # перевіряємо, щоб папка не була тією в яку ми складаємо вже файли
            if item.name not in ('images', 'video', 'documents', 'audio', 'archives', 'others'):
                FOLDERS.append(item)
                # скануємо вкладену папку
                scan(item)  # рекурсія
            continue  # переходимо до наступного елементу в сканованій папці

        # Робота з файлом
        ext = get_extension(item.name)  # беремо розширення файлу
        # ext = item.name.suffix[1:]
        fullname = folder / item.name  # беремо шлях до файлу
        if not ext:  # якщо файл немає розширення то додаєм до невідомих
            OTHERS.append(fullname)
        else:
            try:
                container = REGISTER_EXTENSION[ext]
                EXTENSION.add(ext)
                container.append(fullname)
            except KeyError:
                # Якщо ми не зареєстрували розширення у REGISTER_EXTENSION, то додаємо до невідомих
                UNKNOWN.add(ext)
                OTHERS.append(fullname)


# if __name__ == "__main__":
#     folder_to_scan = sys.argv[1] # py sort.py garbage
#     print(f'Start in folder {folder_to_scan}')
#     scan(Path(folder_to_scan))
#     print(f'Images files: {IMAGES}')
#     print(f'Videos files: {VIDEO}')
#     print(f'Documents files: {DOCS}')
#     print(f'Audio files: {AUDIO}')
#     print(f'Archives files: {ARCHIVES}')

#     print(f'Types of files in folder: {EXTENSION}')
#     print(f'Unknown types of files: {UNKNOWN}') # невідомі типи файлів
#     print(f'OTHERS: {OTHERS}') # папка з невідомими файлами

# main part
def handle_media(filename: Path, target_folder: Path) -> None:
    target_folder.mkdir(exist_ok=True, parents=True) # создаем папку
    filename.replace(target_folder / normalize(filename.name)) # перейменовуэмо назву файлу

def handle_archive(filename: Path, target_folder: Path) -> None:
    target_folder.mkdir(exist_ok=True, parents=True)  # робимо папку для архіва
    folder_for_file = target_folder / normalize(filename.name.replace(filename.suffix, ''))
    folder_for_file.mkdir(exist_ok=True, parents=True)
    try:
        shutil.unpack_archive(filename, folder_for_file)
        # filename.replace(folder_for_file / normalize(filename.name))
    except shutil.ReadError:
        print('It is not archive')
        folder_for_file.rmdir()
    filename.unlink() # удаляє файл

def handle_folder(folder: Path):
    try:
        folder.rmdir()
    except OSError:
        print(f"Can't delete folder: {folder}")

def main(folder: Path):
    scan(folder)
    for file in IMAGES:
        handle_media(file, folder / 'images')
    for file in VIDEO:
        handle_media(file, folder / 'video')
    for file in DOCS:
        handle_media(file, folder / 'documents')
    for file in AUDIO:
        handle_media(file, folder / 'audio')
    for file in ARCHIVES:
        handle_archive(file, folder / 'archives')
    for file in OTHERS:
        handle_media(file, folder / 'others')
    

    for folder in FOLDERS[::-1]:
        handle_folder(folder)

def run():
    aa = input ('Enter path to the folder: ')    
    try:
        folder_for_scan = Path(aa)
        print(f'Cleaning in folder: {folder_for_scan.resolve()}')
        main(folder_for_scan.resolve())
    except FileNotFoundError:
        print('Folder does not exist')



if __name__ == "__main__":
    run()

# запуск файлу main:  py clean_folder_mkv/clean_folder_mkv/clean.py /Users/Maryna/Desktop/garbage 
# запуск файлу main:  py clean_folder_mkv/clean_folder_mkv/clean.py garbage
# c:/garbage
# py clean_folder_mkv/clean.py /Users/Maryna/Desktop/garbage