import json
import matplotlib.pyplot as plt

def plot_team_scores(plot_height=6, plot_width=8):

    with open('TeamScores.json', 'r') as f:
        data = json.load(f)

    org_data = data['ORG_few-shots']
    pw_data = data['PW_few-shots']

    teams = range(len(org_data))


    org_scores = [team_data['normalized_team_score'] for team_data in org_data.values()]
    pw_scores = [team_data['normalized_team_score'] for team_data in pw_data.values()]

    print(org_scores)

    # Create figure and axis objects with specified height and width
    fig, ax1 = plt.subplots(figsize=(plot_width, plot_height))

    # Plot the first set of data (ORG_few-shots) on the left y-axis
    ax1.plot(teams, org_scores, color=plt.cm.tab20c(0), label='The Organizer')  # Use the first color from tab20c colormap
    ax1.set_ylabel('Normalized Prompt Score', color='black', fontsize=9)
    ax1.tick_params(axis='y', labelcolor='black')
    ax1.set_ylim([0, 10])

    # Create a second y-axis on the right side
    ax2 = ax1.twinx()

    # Plot the second set of data (PW_few-shots) on the right y-axis
    ax2.plot(teams, pw_scores, color=plt.cm.tab20c(4), label='Prompt_Wranglers')  # Use the second color from tab20c colormap
    ax2.tick_params(axis='y', labelcolor='black')
    ax2.set_ylim([0, 10])

    # Set x-axis ticks and labels without 'ORG_' string
    team_names = [team.replace('ORG_', '') for team in org_data.keys()]
    ax1.set_xticks(teams)
    ax1.set_xticklabels(teams, rotation=90, fontsize=9)

    # Add grid lines with reduced intensity
    ax1.grid(True, alpha=0.3)
    ax2.grid(True, alpha=0.3)

    # Add legend with fontsize set to 7
    lines, labels = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax2.legend(lines + lines2, labels + labels2, loc='upper left', fontsize=8)

    # Show plot
    plt.tight_layout()
    plt.show()

# Usage:
plot_height = 3
plot_width = 4
plot_team_scores(plot_height, plot_width)
