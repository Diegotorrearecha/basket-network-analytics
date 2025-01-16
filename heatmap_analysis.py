import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

file_path = "CSV_definitive.csv"  # Path to the CSV file
data = pd.read_csv(file_path)  # Load the CSV into a DataFrame

# Filter data based on ResultAction and Action type
successful_shots = data[(data['ResultAction'] == 'SUCCESS') & (data['Action'] == 'SHOOT')]  # Successful shots
failed_shots = data[(data['ResultAction'] == 'FAIL') & (data['Action'] == 'SHOOT')]  # Failed shots
successful_passes = data[(data['ResultAction'] == 'SUCCESS') & (data['Action'] == 'PASS')]  # Successful passes
failed_passes = data[(data['ResultAction'] == 'FAIL') & (data['Action'] == 'PASS')]  # Failed passes

# Create heatmap matrices for successful and failed shots
zones = ["a", "b", "c", "d", "e"]  # Valid zones on the court
columns = ["1", "2", "3", "4"]  # Valid columns on the court

heatmap_successful_shots = pd.DataFrame(0, index=zones, columns=columns)  # Initialize heatmap for successful shots
heatmap_failed_shots = pd.DataFrame(0, index=zones, columns=columns)  # Initialize heatmap for failed shots

# Function to validate if a position is within valid zones and columns
def is_valid_position(position):
    if isinstance(position, str) and len(position) == 2:  # Ensure the position is a string of length 2
        zone, col = position[0], position[1]  # Split into zone and column
        return zone in zones and col in columns  # Check if they are valid
    return False

# Add successful shots to the heatmap
for index, row in successful_shots.iterrows():
    if is_valid_position(row['InitialPosition']):  # Check if the position is valid
        zone = row['InitialPosition'][0]
        col = row['InitialPosition'][1]
        heatmap_successful_shots.loc[zone, col] += 1  # Increment the count in the heatmap

# Add failed shots to the heatmap
for index, row in failed_shots.iterrows():
    if is_valid_position(row['InitialPosition']):
        zone = row['InitialPosition'][0]
        col = row['InitialPosition'][1]
        heatmap_failed_shots.loc[zone, col] += 1

# Create heatmap matrices for successful and failed passes
heatmap_successful_passes = pd.DataFrame(0, index=zones, columns=columns)  # Heatmap for successful passes
heatmap_failed_passes = pd.DataFrame(0, index=zones, columns=columns)  # Heatmap for failed passes

# Add successful passes to the heatmap
for index, row in successful_passes.iterrows():
    if is_valid_position(row['InitialPosition']) and is_valid_position(row['FinalPosition']):  # Validate both positions
        start_zone = row['InitialPosition'][0]
        start_col = row['InitialPosition'][1]
        end_zone = row['FinalPosition'][0]
        end_col = row['FinalPosition'][1]
        heatmap_successful_passes.loc[start_zone, start_col] += 1  # Increment start position count
        heatmap_successful_passes.loc[end_zone, end_col] += 1  # Increment end position count

# Add failed passes to the heatmap
for index, row in failed_passes.iterrows():
    if is_valid_position(row['InitialPosition']) and is_valid_position(row['FinalPosition']):
        start_zone = row['InitialPosition'][0]
        start_col = row['InitialPosition'][1]
        end_zone = row['FinalPosition'][0]
        end_col = row['FinalPosition'][1]
        heatmap_failed_passes.loc[start_zone, start_col] += 1
        heatmap_failed_passes.loc[end_zone, end_col] += 1

# Visualization of heatmaps
fig, axs = plt.subplots(2, 2, figsize=(12, 10))  # Create a 2x2 grid of subplots

sns.heatmap(heatmap_successful_shots, annot=True, fmt="d", cmap="Blues", ax=axs[0, 0])  # Heatmap for successful shots
axs[0, 0].set_title("Tiros Exitosos")  # Title for the heatmap

sns.heatmap(heatmap_failed_shots, annot=True, fmt="d", cmap="Reds", ax=axs[0, 1])  # Heatmap for failed shots
axs[0, 1].set_title("Tiros Fallidos")

sns.heatmap(heatmap_successful_passes, annot=True, fmt="d", cmap="Greens", ax=axs[1, 0])  # Heatmap for successful passes
axs[1, 0].set_title("Pases Exitosos")

sns.heatmap(heatmap_failed_passes, annot=True, fmt="d", cmap="Purples", ax=axs[1, 1])  # Heatmap for failed passes
axs[1, 1].set_title("Pases Fallidos")

plt.tight_layout()  # Adjust the layout for better visualization
plt.show()  # Display the heatmaps
