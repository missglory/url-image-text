import os
import sys

def generate_markdown(txt_folder, img_folder, output_file='assets.md'):
    # Initialize the markdown content
    markdown_content = ''

    # Function to traverse folders recursively and generate markdown
    def traverse_folders(txt_path, img_path, level=1):
        nonlocal markdown_content
        folder_name = os.path.basename(txt_path)
        if level > 1:
            markdown_content += f'{"#" * level} {folder_name}\n'
        
        for txt_item, img_item in zip(os.listdir(txt_path), os.listdir(img_path)):
            txt_item_path = os.path.join(txt_path, txt_item)
            img_item_path = os.path.join(img_path, img_item)
            if os.path.isdir(txt_item_path) and os.path.isdir(img_item_path):
                traverse_folders(txt_item_path, img_item_path, level + 1)
            elif os.path.isfile(txt_item_path) and txt_item.endswith('.txt'):
                with open(txt_item_path, 'r') as file:
                    markdown_content += f'\n{file.read()}\n'
            elif os.path.isfile(img_item_path) and (img_item.endswith('.jpg') or img_item.endswith('.png')):
                markdown_content += f'\n![{img_item}]({os.path.relpath(img_item_path, os.path.dirname(output_file))})\n'
        
        markdown_content += '\n'

    # Traverse both txt and img folders
    traverse_folders(txt_folder, img_folder)

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
