import json
import base64
import sys
import os
from argparse import ArgumentParser

def extract_jpg_responses(input_folder_path, output_folder_path):
    try:
        for filename in os.listdir(input_folder_path):
            if filename.endswith(".har"):
                har_file_path = os.path.join(input_folder_path, filename)
                with open(har_file_path, 'r') as har_file:
                    har_data = json.load(har_file)
                    
                    # Create subfolder corresponding to HAR filename
                    har_subfolder_path = os.path.join(output_folder_path, filename.replace('.har', ''))
                    os.makedirs(har_subfolder_path, exist_ok=True)
                    
                    for entry in har_data['log']['entries']:
                        response = entry['response']
                        
                        # Check if the response contains image/jpeg content
                        if 'content' in response and 'mimeType' in response['content'] and response['content']['mimeType'] == 'image/jpeg':
                            # Extract the content. Note: The content is usually encoded.
                            content = response['content']['text']
                            
                            # Decode base64 encoded content
                            decoded_content = base64.b64decode(content)
                            
                            # Get the URL from the entry
                            url = entry['request']['url']
                            # Replace special characters in the URL to make it a valid filename
                            jpg_filename = url.replace('/', '_').replace(':', '_') + '.jpg'
                            jpg_file_path = os.path.join(har_subfolder_path, jpg_filename)
                            
                            # Save the decoded content to a JPG file
                            with open(jpg_file_path, 'wb') as jpg_file:
                                jpg_file.write(decoded_content)
                                
                            print(f"JPG response data saved to {jpg_file_path}")
                            
    except FileNotFoundError:
        print(f"Folder {input_folder_path} not found.")
    except json.JSONDecodeError as e:
        print(f"Failed to parse JSON: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    parser = ArgumentParser(description="Extract JPG response data from HAR files in a folder and save it to JPG files.")
    parser.add_argument("input_folder_path", help="Path to the folder containing HAR files")
    parser.add_argument("output_folder_path", help="Path to the output folder where JPG files will be saved")
    args = parser.parse_args()
    
    extract_jpg_responses(args.input_folder_path, args.output_folder_path)