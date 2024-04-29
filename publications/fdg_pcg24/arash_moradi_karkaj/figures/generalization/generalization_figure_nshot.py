import json
import matplotlib.pyplot as plt

# For Type2 Fonts (ACM)
plt.rcParams['pdf.fonttype'] = 42
plt.rcParams['ps.fonttype'] = 42

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

def plot_team_scores(plot_height=6, plot_width=8):
    with open('generalization_results_nshot.json', 'r') as f:
        data = json.load(f)

    org_data = data['ORG_few-shots']
    pw_data = data['PW_few-shots']

    org_scores = [compute_raw_score(experiments['characters']) for experiments in org_data.values()]
    pw_scores =  [compute_raw_score(experiments['characters']) for experiments in pw_data.values()]

    fig, ax = plt.subplots(figsize=(plot_width, plot_height))

    shots = range(len(org_scores))
    ax.plot(shots, org_scores, color=plt.cm.tab20c(0), label='The Organizer')
    ax.plot(shots, pw_scores, color=plt.cm.tab20c(4), label='Prompt_Wranglers')

    ax.tick_params(axis='y', labelcolor='black')
    ax.set_ylabel('Raw Score', color='black', fontsize=9)
    ax.set_xlabel('Num. Shots in Prompt', color='black', fontsize=9)
    #ax.set_xticks(shots)
    #ax.set_xticklabels(shots, rotation=90, fontsize=9)

    # Add grid lines with reduced intensity
    ax.grid(True, alpha=0.3)

    # Add legend with fontsize set to 7
    lines, labels = ax.get_legend_handles_labels()
    ax.legend(lines, labels, loc='upper left', fontsize=8)

    # Show plot
    plt.tight_layout()
    plt.savefig("nshot-generalization.pdf")
    plt.show()

# Usage:
plot_height = 3
plot_width = 4
plot_team_scores(plot_height, plot_width)
