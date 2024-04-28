'''
this script takes "data.json" as input and performs score and ranking.
input: "data.json"
output: "TeamRankings_All.xlsx" and "TeamScores.json"
'''

import json
import pandas as pd
import numpy as np

def calculate_total(data, ds):
    for shot, teams in data.items():
        ds[shot] = {}
        for team, chars in teams.items():
            ds[shot][team] = {'total_team_score': 0, 'characters': {}}
            sorted_chars = sorted(chars.items(), key=lambda x: x[0])
            for char, values in sorted_chars:
                similarities = values['similarities']
                stabilities = values['stabilities']
                total_char_sum = 0
                char_data = {'total_char_sum': 0, 'similarity_scores': [], 'stability_scores': []}
                if any(np.isnan(similarities)) or any(np.isnan(stabilities)) or not similarities or not stabilities:
                    continue
                
                if len(similarities) != len(stabilities):
                    continue
                
                number_of_trials = len(similarities)
                
                for sim, stab in zip(similarities, stabilities):
                    trial_score = (sim * stab)
                    char_data['similarity_scores'].append(sim)
                    char_data['stability_scores'].append(stab)
                    total_char_sum += trial_score
                char_data['total_char_sum'] = total_char_sum
                char_data['number_of_trials'] = number_of_trials
                ds[shot][team]['characters'][char] = char_data
                
                mean_similarity = np.mean(char_data['similarity_scores'])
                std_similarity = np.std(char_data['similarity_scores'])
                mean_stability = np.mean(char_data['stability_scores'])
                std_stability = np.std(char_data['stability_scores'])
                
                char_stats = {
                    'total_char_sum': total_char_sum,
                    'mean_similarity': mean_similarity,
                    'std_similarity': std_similarity,
                    'mean_stability': mean_stability,
                    'std_stability': std_stability,
                    'number_of_trials': number_of_trials
                }
                ds[shot][team]['characters'][char].update(char_stats)
                
                ds[shot][team]['total_team_score'] += total_char_sum
    return ds

def rank_teams(data):
    with pd.ExcelWriter("TeamRankings_All.xlsx") as writer:
        for shot, teams in data.items():
            ranked_teams = []
            for team, info in teams.items():
                ranked_teams.append({'Team': team, 'Total_Team_Score': info['total_team_score'], 'Normalized_Team_Score': info.get('normalized_team_score', 0)})
            ranked_teams.sort(key=lambda x: x['Total_Team_Score'], reverse=True)
            df = pd.DataFrame(ranked_teams)
            df.to_excel(writer, sheet_name=shot, index=False)

def normalized_score(data):
    normalized_scores = {}
    for shot, teams in data.items():
        total_score_per_shot = sum(info['total_team_score'] for info in teams.values())
        for team, info in teams.items():
            normalized_team_score = (info['total_team_score'] / total_score_per_shot) * 100
            if team not in normalized_scores:
                normalized_scores[team] = {}
            normalized_scores[team][shot] = normalized_team_score
            data[shot][team]['normalized_team_score'] = normalized_team_score
    with open("TeamScores.json", "w") as json_file:
        json.dump(data, json_file, indent=4)
    return normalized_scores

def main():
    with open("data.json", "r") as f:
        data = json.load(f)

    ds = {}

    result = calculate_total(data, ds)

    with open("TeamScores.json", "w") as json_file:
        json.dump(result, json_file, indent=4)

    normalized_score(result)
    rank_teams(result)

if __name__ == "__main__":
    main()