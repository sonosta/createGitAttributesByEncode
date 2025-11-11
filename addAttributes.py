import os
import sys
import chardet
from pathlib import Path

def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        raw_data = f.read(1024)  # читаем первые 1024 байта для анализа
    result = chardet.detect(raw_data)
    return result['encoding']

def recursive_encoding_check(folder):
    arr_strings = []
    for root, dirs, files in os.walk(folder):
        for file in files:
            file_path = os.path.join(root, file)
            encoding = detect_encoding(file_path)

            encoding_str = encoding if encoding is not None else ""
            extension = Path(file_path).suffix
            short_path = str(Path(file_path).relative_to(folder)).replace('\\', '/')
            if encoding_str != "" and extension in ['.cod', '.mtl', '.lis', '.tpl', '.bro'] :
                if 'windows-' in encoding_str.lower() :
                    encoding_str = encoding_str.replace('windows-', 'cp') + ' eol=crlf'
                file_path = short_path
                arr_strings.append(file_path  + " working-tree-encoding=" + encoding_str + "\n")
            
            print(f"File: {file_path}, Encoding: {encoding}, Short path: {short_path}")
            
    with open(".gitattributes", "w", encoding="utf-8") as f:
        f.writelines(arr_strings)

# Проверяем указанные аргументы при запуске скрипта

if len(sys.argv) <= 1:
    print("Укажите папку по которой будет осуществляться поиск. Пример запуска 'python addAttributes.py `C:\\TESTGIT\\Projects`'")
else:
    print(sys.argv[1])
    folder_path = sys.argv[1]
    recursive_encoding_check(folder_path)