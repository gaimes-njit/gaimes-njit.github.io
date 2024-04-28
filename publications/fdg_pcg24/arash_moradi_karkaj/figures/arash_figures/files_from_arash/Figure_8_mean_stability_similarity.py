import json
import numpy as np
import matplotlib.pyplot as plt

# Step 1: Read JSON file
with open('TeamScores.json') as f:
    data = json.load(f)

# Step 2: Extract relevant information
team_data = data['100run_OG_comp']
team_names = list(team_data.keys())

# Filter out excluded teams
excluded_teams = ['logs', 'pixelArt', 'BirdsTeam', 'BirdBirdBird']
filtered_team_names = [team for team in team_names if team not in excluded_teams]

# Initialize data structures for mean stability and mean similarity calculations
similarity_data = []
stability_data = []

# Step 3: Calculate overall similarity and stability mean for each team
for team in filtered_team_names:
    characters = team_data[team]['characters']
    similarity_scores = []
    stability_scores = []
    num_trials = []
    for char_data in characters.values():
        if not np.isnan(char_data['mean_similarity']):
            similarity_scores.append(char_data['mean_similarity'])
            num_trials.append(char_data['number_of_trials'])
        if not np.isnan(char_data['mean_stability']):
            stability_scores.append(char_data['mean_stability'])
    
    if similarity_scores and num_trials:
        weighted_similarity_mean = np.average(similarity_scores, weights=num_trials)
        similarity_std_dev = np.sqrt(np.average((similarity_scores - weighted_similarity_mean) ** 2, weights=num_trials))
        similarity_data.append((team, weighted_similarity_mean, similarity_std_dev, team_data[team]['normalized_team_score']))
    else:
        similarity_data.append((team, 0, 0, team_data[team]['normalized_team_score']))
    
    if stability_scores and num_trials:
        weighted_stability_mean = np.average(stability_scores, weights=num_trials)
        stability_std_dev = np.sqrt(np.average((stability_scores - weighted_stability_mean) ** 2, weights=num_trials))
        stability_data.append((team, weighted_stability_mean, stability_std_dev, team_data[team]['normalized_team_score']))
    else:
        stability_data.append((team, 0, 0, team_data[team]['normalized_team_score']))

# Sort data based on normalized team scores
similarity_data.sort(key=lambda x: x[3])
stability_data.sort(key=lambda x: x[3])

# Extract sorted team names and corresponding values
sorted_similarity_team_names = [entry[0] for entry in similarity_data]
sorted_similarity_means = [entry[1] for entry in similarity_data]
sorted_similarity_std_devs = [entry[2] for entry in similarity_data]
sorted_similarity_scores = [entry[3] for entry in similarity_data]

sorted_stability_team_names = [entry[0] for entry in stability_data]
sorted_stability_means = [entry[1] for entry in stability_data]
sorted_stability_std_devs = [entry[2] for entry in stability_data]
sorted_stability_scores = [entry[3] for entry in stability_data]

# Step 5: Plot the teams on separate charts
fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(10, 10))

# Plot mean similarity with error bars
cmap = plt.get_cmap('magma')
normalize = plt.Normalize(vmin=0, vmax=1)
sc = axes[0].scatter(sorted_similarity_means, sorted_similarity_team_names, c=sorted_similarity_means, cmap=cmap, norm=normalize, s=301)
axes[0].errorbar(sorted_similarity_means, sorted_similarity_team_names, xerr=sorted_similarity_std_devs, fmt='o', color='black', alpha=0.5, markersize=3)
cbar = plt.colorbar(sc, ax=axes[0])
cbar.set_label('number of successful trials', fontsize=10)
cbar.ax.tick_params(labelsize=10)  # Reduce colorbar tick label size
# axes[0].set_xlabel('Mean Similarity')
axes[0].set_xlim(0, 1)  # Adjust x-axis limit
axes[0].set_title('Mean Similarity', fontsize=10)  # Increase title font size
axes[0].tick_params(axis='both', which='major', labelsize=10)  # Increase tick label font size
axes[0].grid(True, axis='both')

# Plot mean stability with error bars
sc = axes[1].scatter(sorted_stability_means, sorted_stability_team_names, c=sorted_stability_means, cmap=cmap, norm=normalize, s=301)
axes[1].errorbar(sorted_stability_means, sorted_stability_team_names, xerr=sorted_stability_std_devs, fmt='o', color='black', alpha=0.5, markersize=3)
cbar = plt.colorbar(sc, ax=axes[1])
cbar.set_label('number of successful trials', fontsize=10)
cbar.ax.tick_params(labelsize=10)  # Reduce colorbar tick label size
# axes[1].set_xlabel('Mean Stability')
axes[1].set_xlim(0, 1)  # Adjust x-axis limit
axes[1].set_title('Mean Stability', fontsize=10)  # Increase title font size
axes[1].tick_params(axis='both', which='major', labelsize=10)  # Increase tick label font size
axes[1].grid(True, axis='both')

# Manually adjust height and width of the chart
fig.set_figheight(6)
fig.set_figwidth(5)

plt.tight_layout()
plt.show()
