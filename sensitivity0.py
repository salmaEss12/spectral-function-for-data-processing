import numpy as np
import pandas as pd

# Load intensity data directly from CSV files
# Replace 'path_to_signal_intensities.csv' and 'path_to_noise_intensities.csv' with your actual file paths
signal_intensities = pd.read_csv('path_to_signal_intensities.csv', header=None).values.flatten()
noise_intensities = pd.read_csv('path_to_noise_intensities.csv', header=None).values.flatten()

# Assuming uniform spacing or spacing irrelevant, simply sum the squares of the intensities for power
power_signal = np.sum(signal_intensities**2)
power_noise = np.sum(noise_intensities**2)

# Calculate Signal-to-Noise Ratio (SNR)
snr = power_signal / power_noise

print(f"Power of Signal: {power_signal}")
print(f"Power of Noise: {power_noise}")
print(f"Signal-to-Noise Ratio (SNR): {snr}")
