### 4. Text detection ###

# import pytesseract
from PIL import Image
from easyocr import Reader
# import boto3


reader = Reader(['ru'])

# access_key = None
# secret_access_key = None

# textract_client = boto3.client('textract',
#                                aws_access_key_id=access_key,
#                                aws_secret_access_key = secret_access_key,
#                                region_name='us-east-1')


# def read_text_tesseract(image_path):

#   text = pytesseract.image_to_string(Image.open(image_path), lang='eng')
#   fp = f'{image_path}_tsrct.txt'
#   print(fp)
#   with open(fp, 'w+') as wb:
#     wb.write(text)
#   return text

def read_text_easyocr(image_path):
  text = ''
  results = reader.readtext(Image.open(image_path))
  print(results)
  for result in results:
    text = text + result[1] +  ' '

  text = text[:-1]
  fp = f'{image_path}_ocr.txt'
  print(fp)
  with open(fp, 'w+') as wb:
    wb.write(text)
  return text

# def read_text_textract(image_path):

#   with open(image_path, 'rb') as im:
#     response = textract_client.detect_document_text(Document={'Bytes':im.read()})

#   text = ''
#   for item in response['Blocks']:
#     if item['BlockType'] == 'LINE':
#       text = text + item['Text'] + ' '

#   text = text[:-1]

#   return text
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


score_tesseract = 0
score_easyocr = 0
score_textract = 0
path = '/home/mg/aider/url-img-text/traces/'
for image_path_ in os.listdir(path):
  if not '.jpg' in image_path_[-5:]:
    continue
  # print(image_path_)
  image_path = os.path.join(path, image_path_)

  gt = image_path[:-4].replace('_', ' ').lower()

  txt = read_text_easyocr(image_path=image_path)
  print(txt)


# print('score tesseract:', score_tesseract / 100)
# print('score_easyocr:', score_easyocr / 100)
# print('score_textract:', score_textract / 100)
