import sys
import re
import json

def find_urls_in_text(text):
    url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    urls = re.findall(url_pattern, text)
    return urls

def find_urls(filename):
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
    with open('result.json', 'w') as file:
        json.dump(result, file)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python url_finder.py <filename>")
    else:
        filename = sys.argv[1]
        urls = find_urls(filename)
        for url in urls:
            print(url)
        save_urls_to_json(urls, filename)
