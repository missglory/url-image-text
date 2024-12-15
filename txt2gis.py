import argparse
import re
import json
import os

def extract_coordinates(text):
    """
    Extracts coordinates from a given text.
    
    Parameters:
    - text: The string to search for coordinates.
    
    Returns:
    - A list of tuples (longitude, latitude) if found, otherwise an empty list.
    """
    pattern = r"(-?\d{2}\.\d{3,6})[,\s]+(-?\d{2}\.\d{3,6})"
    matches = re.findall(pattern, text)
    
    coordinates = []
    for match in matches:
        try:
            longitude, latitude = map(float, match)
            coordinates.append((longitude, latitude))
        except ValueError:
            print("Failed to convert coordinates to float.")
            
    return coordinates

def process_folder(input_folder_path, output_folder_path):
    """
    Processes all .txt files in the given folder and saves extracted coordinates into JSON files.
    
    Parameters:
    - input_folder_path: The path to the folder containing .txt files.
    - output_folder_path: The path to the output folder where JSON files will be saved.
    """
    for filename in os.listdir(input_folder_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(input_folder_path, filename)
            with open(file_path, 'r') as file:
                text = file.read()
                coordinates = extract_coordinates(text)
                
                if coordinates:
                    json_filename = f"{filename}.json"
                    json_file_path = os.path.join(output_folder_path, json_filename)
                    
                    with open(json_file_path, 'w') as json_file:
                        json.dump(coordinates, json_file, indent=4)
                        print(f"Coordinates saved to {json_filename}")
                else:
                    print(f"No coordinates found in {filename}")
        elif os.path.isdir(os.path.join(input_folder_path, filename)):
            sub_output_folder_path = os.path.join(output_folder_path, filename)
            os.makedirs(sub_output_folder_path, exist_ok=True)
            process_folder(os.path.join(input_folder_path, filename), sub_output_folder_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extracts coordinates from .txt files and saves them into JSON files.")
    parser.add_argument("-i", "--input_folder", required=True, help="Path to the input folder containing .txt files.")
    parser.add_argument("-o", "--output_folder", required=True, help="Path to the output folder where JSON files will be saved.")
    args = parser.parse_args()
    
    os.makedirs(args.output_folder, exist_ok=True)
    process_folder(args.input_folder, args.output_folder)
