import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

# Load exported CSVs (update the filenames if needed)
mutation_df = pd.read_csv("mutation_effect.csv")
cell_count_df = pd.read_csv("cell_count.csv")

# Assuming the MCS column is named 'MCS'
# Rename columns for easier access if needed
mutation_df.columns = ['MCS', 'mutation_effect']
cell_count_df.columns = ['MCS', 'CoI', 'Laminin', 'Cancer1', 'Cancer2', 
                         'C_Lysed', 'L_Lysed', 'NCoI', 'Immune', 'Apoptotic']

# Find peaks in mutation effect
peaks, _ = find_peaks(mutation_df['mutation_effect'], height=0.01)

# Extract MCS values at those peaks
peak_mcs = mutation_df['MCS'].iloc[peaks].values
peak_effects = mutation_df['mutation_effect'].iloc[peaks].values

# Extract Cancer1 values at those MCS
cancer1_at_peaks = cell_count_df[cell_count_df['MCS'].isin(peak_mcs)]

# ---- Plotting ----
plt.figure(figsize=(12, 6))

# Plot 1: Mutation effect with peaks
plt.subplot(1, 2, 1)
plt.plot(mutation_df['MCS'], mutation_df['mutation_effect'], color='green', label='Mutation Effect')
plt.plot(peak_mcs, peak_effects, 'rx', label='Peaks')
plt.title("Effect of Mutation (Peaks)")
plt.xlabel("MCS")
plt.ylabel("Effect")
plt.legend()

# Plot 2: Cancer1 cell count
plt.subplot(1, 2, 2)
plt.plot(cell_count_df['MCS'], cell_count_df['Cancer1'], color='red', label='Cancer1 Count')
plt.scatter(cancer1_at_peaks['MCS'], cancer1_at_peaks['Cancer1'], color='black', label='At Mutation Peaks')
plt.title("Cancer1 Cell Count")
plt.xlabel("MCS")
plt.ylabel("Cell Count")
plt.legend()

plt.tight_layout()
plt.show()

# Optional: Print values at mutation peaks
print("MCS at mutation peaks and corresponding Cancer1 cell counts:")
print(cancer1_at_peaks[['MCS', 'Cancer1']])