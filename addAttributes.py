import os
import sys
import chardet
from pathlib import Path

skip_dirs = ['BaseInt', 'Com', 'ComData', 'ComExt', 'Net', 'SYS', '.git']

def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        raw_data = f.read(1024)  
    result = chardet.detect(raw_data)
    return result['encoding']

def check_line_endings(file_path, encoding_str):

    with open(file_path, 'rb') as f:
        content = f.read(1024)
    if b'\r\n' in content:
        return 'crlf'
    elif b'\n' in content:
        return 'lf'
    else: 
        return 0

def recursive_encoding_check(folder):
    arr_strings = []
    for root, dirs, files in os.walk(folder):
        print(f"dirs: {root}")
        dirs[:] = [d for d in dirs if d not in skip_dirs]  # удаляем папки для пропуска из списка
        for file in files:
            file_path = os.path.join(root, file)
            extension = Path(file_path).suffix
            if extension in ['.cod', '.mtl', '.lis', '.bro']:
                encoding = detect_encoding(file_path)
                encoding_str = encoding if encoding is not None else ""
                
                short_path = str(Path(file_path).relative_to(folder)).replace('\\', '/')
                if encoding_str != "" :
                    if 'windows-' in encoding_str.lower() :
                        encoding_str = encoding_str.lower().replace('windows-', 'cp') 
                        eol = check_line_endings(file_path, encoding_str)
                        if eol != 0:
                            encoding_str = encoding_str + ' eol='+ eol
                        file_path = short_path
                        arr_strings.append('"'+ file_path + '"' + " working-tree-encoding=" + encoding_str + "\n")
                        # print(f"File: {file_path}, Encoding: {encoding}, Short path: {short_path}, EOL: {eol}")

    with open(".gitattributes", "w", encoding="utf-8") as f:
        f.writelines(arr_strings)

# Проверяем указанные аргументы при запуске скрипта

if len(sys.argv) <= 1:
    print("Укажите папку по которой будет осуществляться поиск. Пример запуска 'python addAttributes.py `C:\\TESTGIT\\Projects`'")
else:
    print(sys.argv[1])
    folder_path = sys.argv[1]
    recursive_encoding_check(folder_path)