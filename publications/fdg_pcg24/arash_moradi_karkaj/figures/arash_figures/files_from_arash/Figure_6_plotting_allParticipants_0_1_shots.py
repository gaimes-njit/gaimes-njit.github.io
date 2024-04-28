import json
import matplotlib.pyplot as plt


def plot_team_scores(plot_height=4, plot_width=4):

    with open("TeamScores - Copy.json", "r") as f:
        data = json.load(f)

    shot_data = {}
    team_colors = {}

    available_colors = list(plt.cm.get_cmap("tab20c").colors)

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
    team_order.reverse()

    for team_name in team_order:
        if team_name not in team_colors:
            team_colors[team_name] = available_colors.pop(
                0
            )  # Assign the first available color

    # # Calculate min and max values for normalization
    # min_value = min(
    #     [
    #         team_data.get("normalized_team_score")
    #         for indent_data in data.values()
    #         for team_data in indent_data.values()
    #     ]
    # )
    # max_value = max(
    #     [
    #         team_data.get("normalized_team_score")
    #         for indent_data in data.values()
    #         for team_data in indent_data.values()
    #     ]
    # )

    for shot_letters, teams in data.items():
        shot_letter = shot_letters[0]

        for team_name, team_data in teams.items():
            original_score = team_data.get("normalized_team_score")

            if shot_letter not in shot_data:
                shot_data[shot_letter] = {"teams": [], "scores": [], "colors": []}

            shot_data[shot_letter]["teams"].append(team_name)
            shot_data[shot_letter]["scores"].append(original_score)
            shot_data[shot_letter]["colors"].append(team_colors[team_name])

            print(f"Team {team_name}: \n \t Normalized Prompt Score = {original_score}")

    fig, ax = plt.subplots(figsize=(plot_width, plot_height))

    # print(f"Grouped Data: {shot_data.keys()}")
    # Plotting
    for shot_letter, single_shot_data in shot_data.items():
        for team_name, color in zip(
            single_shot_data["teams"], single_shot_data["colors"]
        ):
            ax.scatter(
                [shot_letter],
                [
                    single_shot_data["scores"][
                        single_shot_data["teams"].index(team_name)
                    ]
                ],
                c=color,
                s=70,
                zorder=2,
            )  # Increase the size of dots and set zorder to 2

    # Customize plot labels and add legend in the desired order
    handles = [
        plt.Line2D(
            [0],
            [0],
            marker="o",
            color="w",
            label=(
                "The Organizer"
                if team_name == "ORG"
                else "Prompt_Wranglers" if team_name == "PW" else team_name
            ),
            markerfacecolor=team_colors[team_name],
            markersize=10,
        )
        for team_name in team_order
    ]
    ax.legend(handles=handles, bbox_to_anchor=(1, 1), loc="upper left", fontsize=9)

    ax.set_ylabel("Normalized Prompt Score", fontsize=9)
    ax.tick_params(axis="both", which="major", labelsize=9)

    # Add grids behind the dots
    ax.grid(True, alpha=0.3)

    # Adjust tight layout to include the legend
    plt.tight_layout()

    plt.show()


if __name__ == "__main__":
    plot_height = 4
    plot_width = 6

    plot_team_scores(plot_height, plot_width)
