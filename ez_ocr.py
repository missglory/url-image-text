### 4. Text detection ###

# import pytesseract
from PIL import Image
from easyocr import Reader
# import boto3
import os
import argparse

reader = Reader(['en'])

def read_text_easyocr(image_path):
  text = ''
  results = reader.readtext(image_path)
  # print(results)
  for result in results:
    text = text + result[1] +  ' '

  text = text[:-1]
  return text

### 5. Compare performances ###

import os


def jaccard_similarity(sentence1, sentence2):
    # Tokenize sentences into sets of words
    set1 = set(sentence1.lower().split())
    set2 = set(sentence2.lower().split())

    # Calculate Jaccard similarity
    intersection_size = len(set1.intersection(set2))
    union_size = len(set1.union(set2))

    # Avoid division by zero if both sets are empty
    similarity = intersection_size / union_size if union_size != 0 else 0.0

    return similarity

formats = ['jpg']
def traverse_folder_recursively(input_folder, output_folder):
  for root, dirs, files in os.walk(input_folder):
    for file in files:
      if file.split('.')[-1] in formats:
        image_path = os.path.join(os.path.abspath(root), file)
        # print(root, dirs, files)

        print(image_path)

        text = read_text_easyocr(image_path)
        relative_path = os.path.relpath(root, input_folder)
        output_path = os.path.join(output_folder, relative_path)
        os.makedirs(output_path, exist_ok=True)
        with open(os.path.join(output_path, file[:-4] + '.txt'), 'w') as f:
          f.write(text)


if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('--input_folder', help='Path to the input folder')
  parser.add_argument('--output_folder', help='Path to the output folder')
  args = parser.parse_args()
  traverse_folder_recursively(args.input_folder, args.output_folder)
