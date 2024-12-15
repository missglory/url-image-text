import os

def traverse_files(directory):
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        if os.path.isdir(item_path):
            print(f"Directory: {item_path}")
            traverse_files(item_path)
        elif os.path.isfile(item_path):
            print(f"File: {item_path}")

# Example usage:
root_directory = '/home/mg/aider/url-img-text/traces/'
traverse_files(root_directory)
