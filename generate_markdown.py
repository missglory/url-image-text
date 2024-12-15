import os
import sys

def generate_markdown(txt_folder, img_folder, output_file='assets.md'):
    # Initialize the markdown content
    markdown_content = ''

    # Function to traverse folders recursively and generate markdown
    def traverse_folders(folder_path, level=1):
        nonlocal markdown_content
        folder_name = os.path.basename(folder_path)
        markdown_content += f'{"#" * level} {folder_name}\n'
        
        for item in os.listdir(folder_path):
            item_path = os.path.join(folder_path, item)
            if os.path.isdir(item_path):
                traverse_folders(item_path, level + 1)
            elif os.path.isfile(item_path):
                if item.endswith('.txt'):
                    with open(item_path, 'r') as file:
                        markdown_content += f'\n{file.read()}\n'
                elif item.endswith('.jpg') or item.endswith('.png'):
                    markdown_content += f'\n![{item}]({os.path.relpath(item_path, os.path.dirname(output_file))})\n'
        
        markdown_content += '\n'

    # Traverse both txt and img folders
    traverse_folders(txt_folder)
    traverse_folders(img_folder)

    # Save the markdown content to the output file
    with open(output_file, 'w') as file:
        file.write(markdown_content)

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python generate_markdown.py <txt_folder_path> <img_folder_path>")
    else:
        txt_folder = sys.argv[1]
        img_folder = sys.argv[2]
        generate_markdown(txt_folder, img_folder)
