import json
import matplotlib.pyplot as plt


import json
import matplotlib.pyplot as plt


def get_team_rankings():
    # Load data from JSON file
    with open("TeamScores - Copy.json", "r") as f:
        data = json.load(f)

    # Initialize dictionaries for data handling
    shot_data = {}

    # Group and sort data by the first letter of shot letters
    for shot_letters, teams in data.items():
        shot_letter = shot_letters[0]
        if shot_letter not in shot_data:
            shot_data[shot_letter] = []

        # Collect all teams and scores for the current shot_letter
        for team_name, team_data in teams.items():
            score = team_data.get("normalized_team_score")
            shot_data[shot_letter].append((team_name, score))

        # Sort teams in the current shot_letter by score in descending order
        shot_data[shot_letter].sort(key=lambda x: x[1], reverse=True)

    # Print and return the rankings
    for shot, teams in shot_data.items():
        print(f"Ranking for shot {shot}:")
        for rank, (team, score) in enumerate(teams, start=1):
            print(f"{rank}. {team} - Score: {score}")

    return shot_data


# Usage
team_rankings = get_team_rankings()


def plot_team_scores(plot_height=4, plot_width=4):
    # Load data from JSON file
    with open("TeamScores - Copy.json", "r") as f:
        data = json.load(f)

    # Initialize dictionaries to store grouped data and colors
    shot_data = {}
    team_colors = {}

    # Define available colors
    available_colors = list(
        plt.cm.get_cmap("tab20c").colors
    )  # Using the 'tab20c' colormap for variety

    # Assign colors to each unique team name and sort them in the desired order
    team_order = [
        "For500",
        "Hope",
        "albatross",
        "JUSTIN",
        "Team Staciiaz",
        "zeilde",
        "Saltyfish1884",
        "Back to the future",
        "Harry Single Group",
        "AdrienTeam",
        "Soda",
        "hachi",
        "PW",
        "dereventsolve",
        "ORG",
    ]
    team_order.reverse()  # Reverse the order of team names

    # Assign colors to teams
    for team_name in team_order:
        team_colors[team_name] = available_colors.pop(0)

    # Group data by the first letter of shot letters and accumulate scores
    for shot_letters, teams in data.items():
        shot_letter = shot_letters[0]
        if shot_letter not in shot_data:
            shot_data[shot_letter] = {"teams": [], "scores": [], "colors": []}

        for team_name, team_data in teams.items():
            original_score = team_data.get("normalized_team_score")
            shot_data[shot_letter]["teams"].append(team_name)
            shot_data[shot_letter]["scores"].append(original_score)
            shot_data[shot_letter]["colors"].append(team_colors[team_name])

    # Create a figure with subplots for each single_shot_data
    num_plots = len(shot_data)
    fig, axs = plt.subplots(1, num_plots, figsize=(plot_width * num_plots, plot_height))

    if num_plots == 1:
        axs = [axs]  # Ensure axs is iterable even if there's only one plot

    # Iterate through each single_shot_data to create separate plots
    for ax, (shot_letter, single_shot_data) in zip(axs, shot_data.items()):
        ax.scatter(
            [shot_letter] * len(single_shot_data["teams"]),
            single_shot_data["scores"],
            c=single_shot_data["colors"],
            s=70,  # Increase the size of dots
            zorder=2,
        )

        # Set the title of each subplot
        ax.set_title(f"Shot {shot_letter}")

        # Customize plot labels
        ax.set_ylabel("Normalized Prompt Score")
        ax.set_xticks([shot_letter])
        ax.set_xticklabels([shot_letter])

        # Add grids
        ax.grid(True, alpha=0.3)

    # Create custom legend for the whole figure
    handles = [
        plt.Line2D(
            [0],
            [0],
            marker="o",
            color="w",
            label=team_name,
            markerfacecolor=team_colors[team_name],
            markersize=10,
        )
        for team_name in team_order
    ]
    fig.legend(handles=handles, bbox_to_anchor=(1.05, 1), loc="upper left")

    # Adjust layout
    plt.tight_layout()

    plt.show()


# Usage
plot_height = 4
plot_width = 6
plot_team_scores(plot_height, plot_width)


import json
import matplotlib.pyplot as plt


def get_top_teams(plot_height=4, plot_width=4):
    # Load data from JSON file
    with open("TeamScores - Copy.json", "r") as f:
        data = json.load(f)

    # Initialize dictionaries for data handling
    shot_data = {}
    top_teams = []

    # Group data by the first letter of shot letters and find the top team
    for shot_letters, teams in data.items():
        shot_letter = shot_letters[0]
        if shot_letter not in shot_data:
            shot_data[shot_letter] = {}

        max_score = -1
        top_team = None

        for team_name, team_data in teams.items():
            score = team_data.get("normalized_team_score")
            if score > max_score:
                max_score = score
                top_team = team_name

        if top_team:
            top_teams.append((shot_letter, top_team, max_score))

    # Print the top teams and their scores
    for shot, team, score in top_teams:
        print(f"Top team for shot {shot}: {team} with score {score}")

    return top_teams


# Usage
top_teams = get_top_teams()
