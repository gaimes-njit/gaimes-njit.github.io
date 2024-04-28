'''
this script is to be placed in the root folder of the full generation directoy, identified in the "root_folder"
and generates "data.json" as output containing stability and similarity score for each team.
'''

import os
import json

root_folder = r"D:\temp\0_1_allParticipants\0_1_all_Participants"
outputFilePath = r"D:\temp\0_1_allParticipants\0_1_all_Participants\Raw_data.txt"

# Define the alphabet
alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

# Define excluded directories
excluded_directories = ["logs", "result"]

# Function to check if the number of values in "similarity" and "stability" are equal
def check_similarity_stability_count(similarity_data, stability_data, letter_shot, team, char):
    similarity_count = len(similarity_data)
    stability_count = len(stability_data)
    if similarity_count != stability_count:
        raise ValueError(f"For {letter_shot}, team {team}, char {char}: Number of 'similarity' values ({similarity_count}) is not equal to number of 'stability' values ({stability_count})")

# Initialize data dictionary
data = {}

try:
    for letter_shot in os.listdir(root_folder):
        if letter_shot not in excluded_directories and os.path.isdir(os.path.join(root_folder, letter_shot)):
            data[letter_shot] = {}
            competition_path = os.path.join(root_folder, letter_shot, "competition")
            if os.path.exists(competition_path) and os.path.isdir(competition_path):
                competition_folders = [folder for folder in os.listdir(competition_path) if os.path.isdir(os.path.join(competition_path, folder))]
                for team in competition_folders:
                    data[letter_shot][team] = {}
                    for char in alphabet:
                        similarity_path = os.path.join(root_folder, letter_shot, "competition", team, "similarity")
                        si_filename = f'{char}.json'
                        si_filepath = os.path.join(similarity_path, si_filename)
                        
                        stability_path = os.path.join(root_folder, letter_shot, "competition", team, "stability")
                        st_filename = f'{char}.json'
                        st_filepath = os.path.join(stability_path, st_filename)
                                
                        if os.path.exists(si_filepath) and os.path.exists(st_filepath):
                            with open(si_filepath, 'r') as f1, open(st_filepath, 'r') as f2:
                                similarity_JSON = json.load(f1)
                                stability_JSON = json.load(f2)
                                
                                similarity_data = [trial["similarity"] for trial in similarity_JSON["trials"]]
                                stability_data = [raw["score"] for raw in stability_JSON["raws"]]
                                
                                check_similarity_stability_count(similarity_data, stability_data, letter_shot, team, char)
                                
                                data[letter_shot][team][char] = {"similarities": similarity_data, "stabilities": stability_data}

    formatted_data = json.dumps(data, indent=4)
    print(formatted_data)

    with open("data.json", "w") as json_file:
        json.dump(data, json_file, indent=4)

except ValueError as e:
    print("Error:", e)
    print("Program terminated.")
