import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Read the Excel file
df = pd.read_excel("Prompt_Wranglers_competition_stats.xlsx")

# Group by character and calculate mean and standard deviation for stabilityScore, similarityScore, and total score
characters = sorted(df['character'].unique())

# Stability Score
stability_mean = np.array([df[df['character'] == char]['stabilityScore'].mean() for char in characters])
stability_std = np.array([df[df['character'] == char]['stabilityScore'].std() for char in characters])

# Similarity Score
similarity_mean = np.array([df[df['character'] == char]['similarityScore'].mean() for char in characters])
similarity_std = np.array([df[df['character'] == char]['similarityScore'].std() for char in characters])

# Total Score
total_scores = []
for char in characters:
    char_df = df[df['character'] == char]
    total_char_score = char_df['stabilityScore'] * char_df['similarityScore']
    total_scores.append(total_char_score)

total_scores_mean = np.array([scores.mean() for scores in total_scores])
total_scores_std = np.array([scores.std() for scores in total_scores])

# Plotting all scores in one chart
plt.figure(figsize=(12, 6))

# Stability Score
plt.errorbar(characters, stability_mean, yerr=stability_std, fmt='o', label='stability', color='blue', markerfacecolor='none', capsize=5, lw=1, elinewidth=4, markersize=7)

# Similarity Score
plt.errorbar(characters, similarity_mean, yerr=similarity_std, fmt='o', label='similarity', color='green', markerfacecolor='none', capsize=5, lw=1, elinewidth=3, markersize=10)

# Total Score
plt.errorbar(characters, total_scores_mean, yerr=total_scores_std, fmt='o', label='total score', color='#FF5733', markerfacecolor='none', markersize=15, capsize=5, lw=1, elinewidth=1)

plt.xlabel('Character', fontsize=11)
plt.ylabel('Average Score', fontsize=11)
# plt.title('Mean and Standard Deviation of Scores for each Character', fontsize=12)
plt.legend()
plt.grid(True)
plt.show()
