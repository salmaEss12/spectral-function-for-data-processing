import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from os.path import isfile, join

def read_spectrum(file_path):
    spectrum_data = pd.read_csv(file_path, header=None, sep='\t')
    energy = spectrum_data[0]
    return energy

# Set the pathname to your files directory
pathname = '/Users/salmaessawab/Desktop/snrpixel'  # Replace with the correct path

pixel_numbers = [144, 252, 400, 10200]
snr_values = []
noisepower = []
signalpower = []

# Process each pair of signal and noise files
for pixels in pixel_numbers:
    noise_file = join(pathname, f'noise_{pixels}.txt')
    signal_file = join(pathname, f'signal_{pixels}.txt')

    if isfile(noise_file) and isfile(signal_file):
        noise_energy = read_spectrum(noise_file)
        signal_energy = read_spectrum(signal_file)

        # Calculate the offset and adjust the energy values
        offset = np.mean(noise_energy)
        adjusted_noise_energy = noise_energy - offset
        adjusted_signal_energy = signal_energy - offset

        # Calculate total power for signal and noise using absolute values
        noise_power = np.sum(np.abs(adjusted_noise_energy))
        signal_power = np.sum(np.abs(adjusted_signal_energy))

        # Calculate SNR
        snr = 10*np.log(signal_power / noise_power) if noise_power > 0 else float('inf')
        snr_values.append(snr)
        noisepower.append(noise_power)
        signalpower.append(signal_power)
    else:
        print(f"Files for pixel number {pixels} are missing.")

# Plot SNR vs. number of pixels integrated over with logarithmic y-axis and x-axis
plt.figure(figsize=(10, 6))
plt.loglog(pixel_numbers, snr_values, 'o-', label='SNR (Signal Power / Noise Power)')
plt.xlabel('Number of Pixels Integrated Over')
plt.ylabel('SNR(Db) ')
plt.title('Log-Log Plot of SNR(Db) vs. Number of Pixels Integrated Over')
plt.legend()
plt.grid(True, which="both", ls="--")  # Grid lines suitable for log-log scale
plt.show()

# Print out the SNR, signal power, and noise power values
print("SNR values:", snr_values)
print("Signal power values:", signalpower)
print("Noise power values:", noisepower)
