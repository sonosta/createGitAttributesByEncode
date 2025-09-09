import os
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
            if encoding_str != "" and extension in ['.txt', '.md', '.json', '.xml', '.html'] :
                arr_strings.append('"'+ file_path + '"' + " working-tree-encoding=" + encoding_str + "\n")
            
            print(f"File: {file_path}, Encoding: {encoding}")
            
    with open("output.txt", "w", encoding="utf-8") as f:
        f.writelines(arr_strings)

# Использование:
folder_path = "C:\\Users\\user\\Desktop\\zapret-win-bundle-master"
recursive_encoding_check(folder_path)