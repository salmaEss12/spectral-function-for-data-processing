import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
from os.path import isfile, join
from scipy.optimize import curve_fit

lambda0 = 632.5  # Assuming lambda0 is known and the same for all files

def read_spectrum(file_path):
    spectrum_data = pd.read_csv(file_path, header=None, sep='\t')
    energy = spectrum_data[0]
    pixels = np.arange(len(energy))
    wavelengths = lambda0 + (pixels - (len(pixels)-1) // 2) * (0.0884)
    return wavelengths, energy

def exp_func(x, a, b):
    return a * np.exp(b * x)

pathname = '/Users/salmaessawab/Downloads/BSc project 2023/SN gain 2'  # Path to the directory with your files

gains = []
snr_values = []
maxSignal = []
noisestd = []
offsets= []

for i in range(0, 49, 4):  # Loop over gain values from 1 to 13
    noise_file = join(pathname, f'noise{i}.txt')
    signal_file = join(pathname, f'SNgain{i}.txt')

    if isfile(noise_file) and isfile(signal_file):
        _, noise_energy = read_spectrum(noise_file)
        offset = np.mean(noise_energy)

        noise_energy -= offset
        _, signal_energy = read_spectrum(signal_file)
        signal_energy -= offset

        noise_std = np.std(noise_energy)
        signal_peak = np.max(signal_energy)
        snr = signal_peak / noise_std if noise_std != 0 else 0

        gains.append(i)
        snr_values.append(snr)
        maxSignal.append(signal_peak)
        noisestd.append(noise_std)
        offsets.append(offset)
    else:
        print(f"Files for gain {i} are missing.")

# Fit the exponential model to the maxSignal, noisestd, and offsets with gain
params_maxSignal, _ = curve_fit(exp_func, np.array(gains), np.array(maxSignal), p0=(1, 0.01))
params_noisestd, _ = curve_fit(exp_func, np.array(gains), np.array(noisestd), p0=(1, 0.01))
params_offsets, _ = curve_fit(exp_func, np.array(gains), np.array(offsets), p0=(1, 0.01))

# Generate fitted data for plotting
fitted_maxSignal = exp_func(np.array(gains), *params_maxSignal)
fitted_noisestd = exp_func(np.array(gains), *params_noisestd)
fitted_offsets = exp_func(np.array(gains), *params_offsets)

# Plotting

# Max Signal and its Exponential Fit
plt.figure(figsize=(10, 6))
plt.plot(gains, maxSignal, 'o', label='Original maxSignal')
plt.plot(gains, fitted_maxSignal, '-', label='Fitted maxSignal')
plt.text(gains[-1], fitted_maxSignal[-1], f"b = {params_maxSignal[1]:.4f}", ha='right')
plt.xlabel('Gain')
plt.ylabel('Max Signal')
plt.title('Max Signal and its Exponential Fit')
plt.legend()
plt.grid(True)
plt.show()

# Noise Std Dev and its Exponential Fit
plt.figure(figsize=(10, 6))
plt.plot(gains, noisestd, 'o', label='Original Noise Std Dev')
plt.plot(gains, fitted_noisestd, '-', label='Fitted Noise Std Dev')
plt.text(gains[-1], fitted_noisestd[-1], f"b = {params_noisestd[1]:.4f}", ha='right')
plt.xlabel('Gain')
plt.ylabel('Noise Std Dev')
plt.title('Noise Std Dev and its Exponential Fit')
plt.legend()
plt.grid(True)
plt.show()

# Offset and its Exponential Fit
plt.figure(figsize=(10, 6))
plt.plot(gains, offsets, 'o', label='Original Offsets')
plt.xlabel('Gain')
plt.ylabel('Offset')
plt.title('Offset and its Exponential Fit')
plt.legend()
plt.grid(True)
plt.show()

# Output the parameters
# Output the parameters
print(f"Max Signal fit parameters: a = {params_maxSignal[0]}, b = {params_maxSignal[1]}")
print(f"Noise Std Dev fit parameters: a = {params_noisestd[0]}, b = {params_noisestd[1]}")
print(f"Offsets fit parameters: a = {params_offsets[0]}, b = {params_offsets[1]}")  # This line was added to complete the code properly.
