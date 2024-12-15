import sys
import os
import re
import json

def find_urls_in_text(text):
    url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    urls = re.findall(url_pattern, text)
    return urls

def find_urls_in_file(filename):
    try:
        with open(filename, 'r') as file:
            text = file.read()
            return find_urls_in_text(text)
    except FileNotFoundError:
        print(f"File {filename} not found.")
        return []

def save_urls_to_json(urls, filename):
    result = {
        "links": urls
    }
    output_folder = sys.argv[2]
    output_filename = os.path.basename(filename) + '.json'
    output_path = os.path.join(output_folder, output_filename)
    with open(output_path, 'w') as file:
        json.dump(result, file)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python url_finder.py <input_folder> <output_folder>")
    else:
        input_folder = sys.argv[1]
        output_folder = sys.argv[2]
        for filename in os.listdir(input_folder):
            if filename.endswith(".txt"):
                filepath = os.path.join(input_folder, filename)
                urls = find_urls_in_file(filepath)
                for url in urls:
                    print(url)
                save_urls_to_json(urls, filename)
