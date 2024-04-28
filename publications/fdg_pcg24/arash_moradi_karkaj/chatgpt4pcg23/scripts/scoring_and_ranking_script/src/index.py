from datetime import datetime
from json2csv import AsyncParser
from bignumber import BigNumber
import os
import json
from pathlib import Path
import asyncio

CHARACTER_LIST = [
    "A",
    "B",
    "C",
    "D",
    "E",
    "F",
    "G",
    "H",
    "I",
    "J",
    "K",
    "L",
    "M",
    "N",
    "O",
    "P",
    "Q",
    "R",
    "S",
    "T",
    "U",
    "V",
    "W",
    "X",
    "Y",
    "Z",
]
STAGE_STABILITY = "stability"
STAGE_SIMILARITY = "similarity"
NUM_TRIALS = 10
CURRENT_STAGE = "result"


class TeamTrialScore:
    def __init__(self, trial_score, character, team, trial):
        self.trial_score = trial_score
        self.character = character
        self.team = team
        self.trial = trial


# Define other classes similarly...


async def main():
    source_folder = ""
    try:
        source_folder = parse_source_folder_argument()
    except Exception as e:
        print(e.message)
        return

    log_folder_path = await create_log_folder(source_folder)
    prompts = await list_all_dirs(source_folder)
    weights = await get_weights(source_folder)

    all_team_trial_scores = []
    all_team_average_stability_scores = []
    all_team_average_similarity_scores = []
    all_team_character_scores = []
    all_team_prompt_scores = []
    all_teams_final_scores_and_ranks = []

    for prompt in prompts:
        team_log = f"[{datetime.now().isoformat()}] Processing - prompt: {prompt}"
        await append_log(log_folder_path, CURRENT_STAGE, team_log)

        prompt_file_path = os.path.join(source_folder, prompt)
        stability = []
        similarity = []

        try:
            stability_path = os.path.join(prompt_file_path, STAGE_STABILITY)
            stability = await list_all_files(stability_path)
        except Exception as e:
            prompt_log = (
                f"[{datetime.now().isoformat()}] Processing - prompt: {prompt} - Failed"
            )
            await append_log(log_folder_path, CURRENT_STAGE, f"{prompt_log} - {str(e)}")

        # Similar try-catch block for similarity

        if len(stability) != len(similarity):
            prompt_log = (
                f"[{datetime.now().isoformat()}] Processing - prompt: {prompt} - Failed"
            )
            await append_log(
                log_folder_path,
                CURRENT_STAGE,
                f"{prompt_log} - Number of stability files and similarity files are not equal.",
            )
            return

        # Rest of the code...


# Define other functions like parse_source_folder_argument, create_log_folder, list_all_dirs, etc...

# If using asyncio, don't forget to run the async main function like this:
asyncio.run(main())
