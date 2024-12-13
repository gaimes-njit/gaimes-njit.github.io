import json
import os

# Define the path to the directory containing the JSON files
json_stability_directory = 'stability'
json_similarity_directory = 'similarity'

# Define the base path to the directory containing the image folders (A, B, etc.)
base_image_directory = 'images'

# Create or open an HTML file for writing
with open('output.html', 'w') as html_file:
    # html boilerplate
    print('''<!DOCTYPE html>
<meta name=viewport content="width=device-width, initial-scale=1">
<meta charset=utf-8>
<style type=text/css>body { max-width: 800px; margin: auto; }</style>''', file=html_file)
    # table start and header
    print('<table><tr><th>Letter</th><th>Tag</th><th>Stability Score</th><th>Similarity Score</th><th>Image Raw</th><th>Image Converted</th></tr>', file=html_file)

    # Loop through characters 'A' to 'Z'
    for char in range(ord('A'), ord('Z') + 1):
        char = chr(char)  # Convert the character code back to a character
        # Construct the file paths for JSON files and image folders
        json_stability_path = os.path.join(json_stability_directory, f'{char}.json')
        json_stability_path = os.path.join(json_stability_directory, f'{char}.json')

        json_similarity_path = os.path.join(json_similarity_directory, f'{char}.json')
        base_image_folder_path = os.path.join(base_image_directory, char)

        # Check if JSON files exist for the current character
        if os.path.exists(json_stability_path) and os.path.exists(json_similarity_path):
            # Read data from the first JSON file
            with open(json_stability_path, 'r') as json_file1, open(json_similarity_path, 'r') as json_file2:
                stability = json.load(json_file1)
                similarity = json.load(json_file2)

            # Construct the path to the current image folder
            if os.path.exists(base_image_folder_path):
                # List all image files in the current folder
                image_files = os.listdir(base_image_folder_path)

                for item1, item2 in zip(stability['raws'], similarity['trials']):
                    tag = item1['tag']
                    stability_score = item1['score']
                    similarity_score = item2['similarity']
                    starting_objects = item1['startingObjects']
                    moving_objects = item1['movingObjects']
                    image_file = item2['id']
                    image_file_raw = image_file[:-4] + "_raw" + ".png"

                    # Write a row to the HTML table
                    print(f"<tr><td>{char}</td><td>{tag}</td><td>{stability_score}</td><td>{similarity_score}</td><td><img src=\"{base_image_folder_path}/{image_file_raw}\" width=30></td><td><img src=\"{base_image_folder_path}/{image_file}\" width=30></td></tr>", file=html_file)
    # close the table
    print("</table>", file=html_file)
