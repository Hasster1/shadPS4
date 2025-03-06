import sys
import os
import re
from concurrent.futures import ThreadPoolExecutor

def process_file(file_path, search_string, insert_string):
    with open(file_path, 'r') as f:
        lines = f.readlines()

    updated_lines = []
    found = False
    for line in lines:
        updated_lines.append(line)
        if found:
            if "{" in line:
                updated_lines.append(insert_string + "\n")
                found = False
        elif search_string in line:
            found = True
            if "{" in line:
                updated_lines.append(insert_string + "\n")
                found = False

    with open(file_path, 'w') as f:
        f.writelines(updated_lines)

def main():
    if len(sys.argv) != 4:
        print("Usage: python3 script.py <folder> <search_string> <insert_string>")
        sys.exit(1)

    folder, search_string, insert_string = sys.argv[1:]
    cpp_files = [os.path.join(root, file) for root, _, files in os.walk(folder) for file in files if file.endswith(".cpp")]

    with ThreadPoolExecutor() as executor:
        executor.map(lambda f: process_file(f, search_string, insert_string), cpp_files)

if __name__ == "__main__":
    main()