import subprocess

def generate_markdown(txt_folder, img_folder):
    command = f"python generate_markdown.py {txt_folder} {img_folder}"
    subprocess.run(command, shell=True)

# Example usage:
generate_markdown("/path/to/txt/folder", "/path/to/img/folder")
