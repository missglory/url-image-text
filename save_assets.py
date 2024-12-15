import os
import argparse
from shutil import copy

def save_text_and_images(txt_folder, img_folder, output_folder):
    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)
    
    # Walk through text folder and copy files to output
    for root, dirs, files in os.walk(txt_folder):
        for file in files:
            if file.endswith(".txt"):
                src_path = os.path.join(root, file)
                dst_path = os.path.join(output_folder, file)
                copy(src_path, dst_path)
                print(f"Text file saved: {file}")
    
    # Walk through image folder and copy files to output
    for root, dirs, files in os.walk(img_folder):
        for file in files:
            if file.endswith(".jpg") or file.endswith(".png"):
                src_path = os.path.join(root, file)
                dst_path = os.path.join(output_folder, file)
                copy(src_path, dst_path)
                print(f"Image saved: {file}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Save text and images from folders.')
    parser.add_argument('txt_folder', type=str, help='Path to the folder containing text files.')
    parser.add_argument('img_folder', type=str, help='Path to the folder containing image files.')
    parser.add_argument('output_folder', type=str, help='Path where the files will be saved.')
    args = parser.parse_args()
    
    save_text_and_images(args.txt_folder, args.img_folder, args.output_folder)
