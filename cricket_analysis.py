import pandas as pd

# Define the dataset columns
columns = [
    'Match No.',
    'Innings',
    'Team',
    'Player Name',
    'Ballcount',
    'Position',
    'Short Description',
    'Pick',
    'Throw',
    'Runs',
    'Overcount',
    'Venue'
]

# Sample data for three players: Virat Kohli, Rohit Sharma, Jasprit Bumrah
# From a fictional T20 match: India vs Australia, Match 1, Innings 1, Team India, Venue Melbourne
data = [
    [1, 1, 'India', 'Virat Kohli', 1, 'Cover', 'Clean pick and throw', 'clean pick', 'run out', 2, 1, 'Melbourne'],
    [1, 1, 'India', 'Rohit Sharma', 3, 'Point', 'Good catch', 'catch', '', 1, 1, 'Melbourne'],
    [1, 1, 'India', 'Jasprit Bumrah', 5, 'Fine Leg', 'Fumble but good throw', 'fumble', 'good throw', 1, 2, 'Melbourne'],
    [1, 1, 'India', 'Virat Kohli', 7, 'Mid Off', 'Dropped catch', 'drop catch', '', -1, 2, 'Melbourne'],
    [1, 1, 'India', 'Rohit Sharma', 9, 'Slip', 'Catch taken', 'catch', '', 1, 3, 'Melbourne'],
    [1, 1, 'India', 'Jasprit Bumrah', 11, 'Square Leg', 'Clean pick, run out', 'clean pick', 'run out', 2, 4, 'Melbourne'],
    [1, 1, 'India', 'Virat Kohli', 13, 'Cover', 'Good throw, missed run out', 'good throw', 'missed run out', -1, 5, 'Melbourne'],
    [1, 1, 'India', 'Rohit Sharma', 15, 'Point', 'Stumping', '', 'stumping', 1, 6, 'Melbourne'],
    [1, 1, 'India', 'Jasprit Bumrah', 17, 'Fine Leg', 'Bad throw', 'bad throw', '', -1, 7, 'Melbourne'],
    [1, 1, 'India', 'Virat Kohli', 19, 'Mid On', 'Direct hit run out', '', 'run out', 2, 8, 'Melbourne'],
    # Add more for completeness, but this is sample
]

# Create DataFrame
df = pd.DataFrame(data, columns=columns)

# Save to Excel
df.to_excel('cricket_fielding_analysis.xlsx', index=False)

print("Dataset created and saved to cricket_fielding_analysis.xlsx")

# Now, calculate performance scores
# First, define weights (assumed)
weights = {
    'CP': 1,  # Clean Picks
    'GT': 1,  # Good Throws
    'C': 2,   # Catches
    'DC': -1, # Dropped Catches
    'ST': 3,  # Stumpings
    'RO': 2,  # Run Outs
    'MRO': -1,# Missed Run Outs
    'DH': 2,  # Direct Hits (assuming same as RO)
    'RS': 1   # Runs Saved (already in Runs)
}

# Function to count categories for each player
def calculate_counts(group):
    counts = {
        'CP': (group['Pick'] == 'clean pick').sum(),
        'GT': (group['Pick'] == 'good throw').sum() + (group['Throw'] == 'good throw').sum(),
        'C': (group['Pick'] == 'catch').sum(),
        'DC': (group['Pick'] == 'drop catch').sum(),
        'ST': (group['Throw'] == 'stumping').sum(),
        'RO': (group['Throw'] == 'run out').sum(),
        'MRO': (group['Throw'] == 'missed run out').sum(),
        'DH': 0,  # Assuming direct hit is run out
        'RS': group['Runs'].sum()
    }
    return counts

# Group by Player Name
grouped = df.groupby('Player Name')

performance_scores = {}
for player, group in grouped:
    counts = calculate_counts(group)
    ps = sum(counts[key] * weights[key] for key in weights)
    performance_scores[player] = {'counts': counts, 'PS': ps}

# Print performance scores
for player, data in performance_scores.items():
    print(f"\nPlayer: {player}")
    print("Counts:", data['counts'])
    print("Performance Score:", data['PS'])

# Save performance to another sheet or file
perf_df = pd.DataFrame.from_dict({k: {**v['counts'], 'PS': v['PS']} for k, v in performance_scores.items()}, orient='index')
perf_df.to_excel('performance_scores.xlsx')

print("\nPerformance scores saved to performance_scores.xlsx")
