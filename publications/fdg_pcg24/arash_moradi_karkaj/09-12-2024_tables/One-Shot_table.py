import json
import csv

# Function to calculate raw scores
def compute_raw_score(results):
    raw_score = 0.0
    for level_results in results.values():
        raw_score += level_results["total_char_sum"] / level_results["number_of_trials"]
    raw_score /= 26.0  # Normalize over 26 shots
    return raw_score

# Team colors and order
def get_team_colors_filtered_for_one_shot():
    teams_with_examples = ['ORG', 'dereventsolve', 'PW', 'hachi', 'Soda', 'AdrienTeam', 'Saltyfish1884', 'For500']
    team_order = teams_with_examples
    return team_order

# Process JSON data into table format
def get_json_data(json_file, team_order):
    with open(json_file, "r") as f:
        data = json.load(f)

    table_data = {}

    for shot_key, shot_data in data.items():
        if shot_key not in table_data:
            table_data[shot_key] = {}
        for team_name, team_results in shot_data.items():
            if team_name in team_order:
                raw_score = compute_raw_score(team_results["characters"])
                table_data[shot_key][team_name] = round(raw_score, 2)

    return table_data

# Save table as CSV file
def save_table_as_csv(table_data, team_order, save_name):
    # Prepare headers
    headers = ['Shot Letter'] + team_order

    # Prepare rows
    rows = []
    for shot_letter, team_scores in sorted(table_data.items()):
        row = [shot_letter] + [team_scores.get(team, '-') for team in team_order]
        rows.append(row)

    # Write to CSV
    with open(save_name, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(headers)
        csv_writer.writerows(rows)

    print(f"CSV table saved to {save_name}")

# Save table as LaTeX format
def save_table_as_latex(table_data, team_order, save_name):
    latex_str = "\\begin{table}[h!]\n\\centering\n\\begin{tabular}{" + ("l" + "r" * len(team_order)) + "}\n"
    latex_str += "Shot Letter & " + " & ".join(team_order) + " \\\\\n"
    latex_str += "\\hline\n"

    # Add rows
    for shot_letter, team_scores in sorted(table_data.items()):
        row = [f"{shot_letter}"] + [f"{team_scores.get(team, '-')}" for team in team_order]
        latex_str += " & ".join(row) + " \\\\\n"

    latex_str += "\\end{tabular}\n\\caption{One-shot Generalization Results}\n\\label{tab:one_shot_generalization}\n\\end{table}"

    with open(save_name, 'w') as latex_file:
        latex_file.write(latex_str)

    print(f"LaTeX table saved to {save_name}")

if __name__ == "__main__":
    json_file_path = 'generalization_results_one_shot.json'
    csv_save_name = 'one-shot-generalization-table.csv'
    latex_save_name = 'one-shot-generalization-table.tex'

    # Get data
    team_order = get_team_colors_filtered_for_one_shot()
    table_data = get_json_data(json_file_path, team_order)

    # Save table as CSV
    save_table_as_csv(table_data, team_order, csv_save_name)

    # Save table as LaTeX
    save_table_as_latex(table_data, team_order, latex_save_name)
