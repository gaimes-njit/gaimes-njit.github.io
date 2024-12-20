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

def get_team_colors_arash_setting():
    team_order = ["For500","Hope","albatross","JUSTIN","Team Staciiaz","zeilde","Saltyfish1884","Back to the future","Harry Single Group","AdrienTeam","Soda","hachi","PW","dereventsolve","ORG",]
    color_map_name = "tab20c"

    available_colors = list(plt.colormaps[color_map_name].colors)
    team_order.reverse()
    team_colors = {}

    for team_name in team_order:
        if team_name not in team_colors:
            team_colors[team_name] = available_colors.pop(0) 

    return team_colors, team_order

def get_team_colors_filtered_for_one_shot():
    teams_with_examples = ['ORG', 'dereventsolve', 'PW', 'hachi', 'Soda', 'AdrienTeam', 'Saltyfish1884', 'For500']
    team_order = teams_with_examples

    available_colors = list(plt.colormaps['Dark2'].colors)

    team_colors = {}

    for team_name in team_order:
        if team_name not in team_colors:
            team_colors[team_name] = available_colors.pop(0) 

    return team_colors, team_order
def get_json_data(json_file, team_colors):
    prompts_with_shots = [
    ('A', 'ORG'),
    ('A', 'AdrienTeam'),
    ('A', 'PW'),
    ('A', 'dereventsolve'),
    ('A', 'hachi'),
    ('A', 'For500'),
    ('B', 'ORG'),
    ('B', 'PW'),
    ('B', 'dereventsolve'),
    ('B', 'For500'),
    ('C', 'ORG'),
    ('C', 'dereventsolve'),
    ('C', 'PW'),
    ('D', 'ORG'),
    ('D', 'PW'),
    ('D', 'dereventsolve'),
    ('D', 'For500'),
    ('E', 'ORG'),
    ('E', 'dereventsolve'),
    ('E', 'PW'),
    ('E', 'Soda'),
    ('E', 'For500'),
    ('F', 'dereventsolve'),
    ('F', 'PW'),
    ('F', 'ORG'),
    ('F', 'For500'),
    ('G', 'ORG'),
    ('G', 'dereventsolve'),
    ('G', 'PW'),
    ('G', 'For500'),
    ('H', 'PW'),
    ('H', 'dereventsolve'),
    ('H', 'ORG'),
    ('H', 'hachi'),
    ('H', 'For500'),
    ('I', 'dereventsolve'),
    ('I', 'PW'),
    ('I', 'ORG'),
    ('I', 'Saltyfish1884'),
    ('I', 'hachi'),
    ('I', 'For500'),
    ('J', 'ORG'),
    ('J', 'PW'),
    ('J', 'dereventsolve'),
    ('J', 'Soda'),
    ('J', 'hachi'),
    ('J', 'For500'),
    ('K', 'ORG'),
    ('K', 'PW'),
    ('K', 'dereventsolve'),
    ('K', 'For500'),
    ('L', 'Soda'),
    ('L', 'PW'),
    ('L', 'ORG'),
    ('L', 'AdrienTeam'),
    ('L', 'dereventsolve'),
    ('L', 'hachi'),
    ('L', 'For500'),
    ('M', 'PW'),
    ('M', 'ORG'),
    ('M', 'dereventsolve'),
    ('M', 'For500'),
    ('N', 'ORG'),
    ('N', 'PW'),
    ('N', 'dereventsolve'),
    ('O', 'ORG'),
    ('O', 'dereventsolve'),
    ('O', 'AdrienTeam'),
    ('O', 'PW'),
    ('O', 'hachi'),
    ('O', 'For500'),
    ('P', 'dereventsolve'),
    ('P', 'ORG'),
    ('P', 'PW'),
    ('P', 'For500'),
    ('Q', 'PW'),
    ('Q', 'ORG'),
    ('Q', 'dereventsolve'),
    ('R', 'ORG'),
    ('R', 'dereventsolve'),
    ('R', 'PW'),
    ('S', 'ORG'),
    ('S', 'dereventsolve'),
    ('S', 'PW'),
    ('S', 'For500'),
    ('T', 'dereventsolve'),
    ('T', 'ORG'),
    ('T', 'PW'),
    ('T', 'hachi'),
    ('T', 'For500'),
    ('U', 'ORG'),
    ('U', 'PW'),
    ('U', 'dereventsolve'),
    ('U', 'hachi'),
    ('U', 'For500'),
    ('V', 'dereventsolve'),
    ('V', 'PW'),
    ('W', 'ORG'),
    ('W', 'dereventsolve'),
    ('W', 'PW'),
    ('W', 'For500'),
    ('X', 'ORG'),
    ('X', 'dereventsolve'),
    ('X', 'PW'),
    ('Y', 'ORG'),
    ('Y', 'PW'),
    ('Y', 'dereventsolve'),
    ('Y', 'For500'),
    ('Z', 'ORG'),
    ('Z', 'PW'),
    ('Z', 'dereventsolve'),
    ('Z', 'For500')]


    with open(json_file, "r") as f:
        data = json.load(f) #<class 'dict'>

    plot_data = {}

    for one_shot_key, one_shot_data in data.items():
        plot_data[one_shot_key] = {"teams": [], "scores": [], "colors": []}
        for prompt_name, prompt_results in one_shot_data.items():
            if (one_shot_key, prompt_name) in prompts_with_shots: 
                raw_score = compute_raw_score(prompt_results["characters"])

                plot_data[one_shot_key]["teams"].append(prompt_name)
                plot_data[one_shot_key]["scores"].append(raw_score)
                plot_data[one_shot_key]["colors"].append(team_colors[prompt_name])
    return plot_data

def save_and_show_plot(plot_data, save_name, team_colors, team_order, plot_height=4, plot_width=4, y_label_font_size=9, x_label_font_size=9, legend_font_size=8, tick_font_size=8, marker_size=9, legend_marker_size=9):

    fig, ax = plt.subplots(figsize=(plot_width, plot_height))

    for shot_letter, single_shot_data in plot_data.items():
        for team_name, color in zip(single_shot_data["teams"], single_shot_data["colors"]):
            ax.scatter([shot_letter],[single_shot_data["scores"][single_shot_data["teams"].index(team_name)]],
                c=color,
                s=marker_size,
                zorder=2,
                marker='o',
            ) 
    
    handles = [plt.Line2D([0],[0],marker="o",color="w",
                          label=("The Organizer" if team_name == "ORG" else "Prompt_Wranglers" if team_name == "PW" else team_name),
                          markerfacecolor=team_colors[team_name],
                          markersize=legend_marker_size,
        )
        for team_name in team_order
    ]

    #bbox_to_anchor=(0.5, 1.05), loc='center', ncol=2
    #ax.legend(handles=handles, bbox_to_anchor=(0.98, 0.98), loc="upper left", fontsize=legend_font_size)
    ax.legend(handles=handles, handlelength=.3, bbox_to_anchor=(0.5, 1.2), loc="center", ncol=3, title="Team Names", fontsize=legend_font_size, title_fontsize=9)

    
    ax.set_ylabel("Raw Score", fontsize=y_label_font_size)
    ax.set_xlabel('One-Shot Letter in Prompt', color='black', fontsize=x_label_font_size)
    ax.tick_params(axis="both", which="major", labelsize=tick_font_size)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(save_name)
    plt.show()

if __name__ == "__main__":
   
    # # Command Line Arguments
    # plot_height = 4
    # plot_width = 8
    # json_file_path = 'generalization_results_one_shot.json'
    # save_name = 'one-shot-generalization.pdf'

    # Plot Parameters
    plot_height = 5
    plot_width = 5
    y_label_font_size= 10
    x_label_font_size=10
    legend_font_size=10
    tick_font_size=10
    marker_size=50
    legend_marker_size=9

    # For Type2 Fonts (ACM)
    plt.rcParams['pdf.fonttype'] = 42
    plt.rcParams['ps.fonttype'] = 42
    plt.rcParams['font.family'] = 'Arial'

    json_file_path = 'generalization_results_one_shot.json'
    save_name = 'one-shot-generalization.pdf'

    # Show Plot Data
    team_colors, team_order = get_team_colors_filtered_for_one_shot()
    plot_data = get_json_data(json_file_path, team_colors)
    save_and_show_plot(plot_data, save_name, team_colors, team_order, plot_height, plot_width, y_label_font_size, x_label_font_size, legend_font_size, tick_font_size,marker_size, legend_marker_size)





# Original Figure 6 Code (But Separated 0 and One-Shot)
# if __name__ == "__main__":
   
#     # Command Line Arguments
#     plot_height = 4
#     plot_width = 6
#     json_file_path = 'generalization_results_one_shot.json'

#     # Show Plot Data
#     team_colors, team_order = get_team_colors_arash_setting()
#     plot_data = get_json_data(json_file_path, team_colors)
#     show_plot(plot_data, team_colors, team_order, plot_height, plot_width)


