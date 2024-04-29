# Generates LaTeX table rows comparing raw scores for the zero-shot versus
# replication experiments

import json

def compute_raw_score(results):
    # 'results' parameter should be the dict under 'characters' in the JSON for
    # a given run, containing {"A" : { ... }, "B" : { ... }}, etc.

    # Raw score differs from the official competition score by
    # being 1) not dynamically weighted (levels are equally weighted),
    # and 2) not normalized to percentage-of-total-score at the end.
    # This makes raw scores from different runs comparable.
    raw_score = 0.0
    for level_results in results.values():
        raw_score += level_results["total_char_sum"] / level_results["number_of_trials"]
    raw_score /= 26.0
    return raw_score


with open('../../replication_experiment/replication_n100_processed.json', 'r') as f:
    replication = json.load(f)
with open('generalization_results_zero_shot.json', 'r') as f:
    zeroshot = json.load(f)

zeroshot_scores = {"The Organizer" if team == "ORG" else "Prompt_Wranglers" if team == "PW" else
                   team: compute_raw_score(results["characters"])
                   for team,results in zeroshot['0'].items()}
replication_scores = {team: compute_raw_score(results["characters"])
                      for team,results in replication['100run_OG_comp'].items()}

ranked_teams = sorted(zeroshot_scores.keys(), key=lambda x: zeroshot_scores[x], reverse=True)
for rank,team in enumerate(ranked_teams):
    print(f"{rank+1} & {zeroshot_scores[team]:5.3f} & {team:<20} & {replication_scores[team]:5.3f} \\\\")
