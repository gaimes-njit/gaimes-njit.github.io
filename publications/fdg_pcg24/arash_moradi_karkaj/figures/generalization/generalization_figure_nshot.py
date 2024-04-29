import json
import matplotlib.pyplot as plt



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

def get_json_data(json_file):
    
    with open(json_file, "r") as f:
        data = json.load(f) 

    org_data = data['ORG_few-shots']
    pw_data = data['PW_few-shots']

    org_scores = [compute_raw_score(experiments['characters']) for experiments in org_data.values()]
    pw_scores =  [compute_raw_score(experiments['characters']) for experiments in pw_data.values()]
    shots = range(len(org_scores))

    return shots, org_scores, pw_scores

   
def save_and_show_plot(shots, org_scores, pw_scores, save_name, plot_height=6, plot_width=8, y_label_font_size=9, x_label_font_size=9, legend_font_size=8, tick_font_size=8):

    fig, ax = plt.subplots(figsize=(plot_width, plot_height))

    ax.plot(shots, org_scores, color=plt.cm.tab20c(0), label='The Organizer')
    ax.plot(shots, pw_scores, color=plt.cm.tab20c(4), label='Prompt_Wranglers')

    ax.tick_params(axis='y', labelcolor='black')
    ax.set_ylabel('Raw Score', color='black', fontsize=y_label_font_size)
    ax.set_xlabel('Num. Shots in Prompt', color='black', fontsize=x_label_font_size)
    ax.tick_params(axis='both', which='both', labelsize=tick_font_size)

    # Add grid lines with reduced intensity
    ax.grid(True, alpha=0.3)

    #
    lines, labels = ax.get_legend_handles_labels()
    ax.legend(lines, labels, loc='upper left', fontsize=legend_font_size)

    # Show plot
    plt.tight_layout()
    plt.savefig(save_name)
    plt.show()


if __name__ == "__main__":
   
    # Plot Parameters
    plot_height = 3
    plot_width = 4
    y_label_font_size= 10
    x_label_font_size=10
    legend_font_size=10
    tick_font_size=10

    # For Type2 Fonts (ACM)
    plt.rcParams['pdf.fonttype'] = 42
    plt.rcParams['ps.fonttype'] = 42
    plt.rcParams['font.family'] = 'Arial'

    json_file_path = 'generalization_results_nshot.json' 
    save_name_path = 'nshot-generalization.pdf'

    # Show Plot Data
    shots, org_scores, pw_scores = get_json_data(json_file_path)
    save_and_show_plot(shots,org_scores,pw_scores, save_name_path, plot_height, plot_width, y_label_font_size, x_label_font_size, legend_font_size, tick_font_size)



# # Usage:
# plot_height = 3
# plot_width = 4
# plot_team_scores(plot_height, plot_width)


