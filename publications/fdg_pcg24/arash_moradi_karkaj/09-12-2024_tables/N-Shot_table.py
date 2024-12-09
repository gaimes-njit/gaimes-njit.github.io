import json
import pandas as pd  # For table generation and formatting

def compute_raw_score(results):
    """
    Compute the raw score for a given run of experiments.
    """
    raw_score = 0.0
    for level_results in results.values():
        raw_score += level_results["total_char_sum"] / level_results["number_of_trials"]
    raw_score /= 26.0
    return raw_score

def get_json_data(json_file):
    """
    Extract and compute raw scores for ORG and PW data from a JSON file.
    """
    with open(json_file, "r") as f:
        data = json.load(f)

    org_data = data['ORG_few-shots']
    pw_data = data['PW_few-shots']

    org_scores = [compute_raw_score(experiments['characters']) for experiments in org_data.values()]
    pw_scores = [compute_raw_score(experiments['characters']) for experiments in pw_data.values()]
    shots = list(range(len(org_scores)))

    return shots, org_scores, pw_scores

def generate_table(shots, org_scores, pw_scores, output_file="results_table.csv"):
    """
    Generate a table from the computed data and save it as a CSV file.
    """
    # Create a DataFrame for the table
    table_data = {
        "Num. Shots": shots,
        "The Organizer RAW Score": org_scores,
        "Prompt Wranglers RAW Score": pw_scores
    }
    df = pd.DataFrame(table_data)

    # Save to a CSV file
    df.to_csv(output_file, index=False)
    print(f"Table saved to {output_file}")

if __name__ == "__main__":
    json_file_path = 'generalization_results_nshot.json'
    output_file_path = 'N-Shot_table.csv'

    # Extract data from JSON
    shots, org_scores, pw_scores = get_json_data(json_file_path)

    # Generate and save the table
    generate_table(shots, org_scores, pw_scores, output_file_path)