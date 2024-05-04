import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from os.path import isfile, join
from scipy.optimize import curve_fit

def read_spectrum(file_path):
    spectrum_data = pd.read_csv(file_path, header=None, sep='\t')
    energy = spectrum_data[0]
    return energy

def exp_func(x, a, b):
    return a * np.exp(b * x)

pathname = '/Users/salmaessawab/Desktop/SNRgain'  # Path to the directory with your files

gains = []
snr_values = []
totalSignalPower = []
totalNoisePower = []
offsets = []

for i in range(8, 49, 4):  # Loop over specified gain values
    noise_file = join(pathname, f'noise{i}.txt')
    signal_file = join(pathname, f'SNgain{i}.txt')

    if isfile(noise_file) and isfile(signal_file):
        noise_energy = read_spectrum(noise_file)
        offset = np.mean(noise_energy)

        noise_energy -= offset
        signal_energy = read_spectrum(signal_file)
        signal_energy -= offset

        total_noise_power = np.sum(np.abs(noise_energy))  # Summing the absolute power of noise
        total_signal_power = np.sum(np.abs(signal_energy))  # Summing the absolute power of signal

        snr = 10*np.log(total_signal_power / total_noise_power) if total_noise_power != 0 else 0

        gains.append(i)
        snr_values.append(snr)
        totalSignalPower.append(total_signal_power)
        totalNoisePower.append(total_noise_power)
        offsets.append(offset)
    else:
        print(f"Files for gain {i} are missing.")

# Since SNR is already calculated, we can directly plot SNR with gain
plt.figure(figsize=(10, 6))
plt.plot(gains, snr_values, 'o-', label='SNR')
plt.xlabel('Gain')
plt.ylabel('SNR')
plt.title('SNR as a Function of Gain')
plt.legend()
plt.grid(True)
plt.show()

# Optional: Plot totalSignalPower and totalNoisePower with gain to see their trends
plt.figure(figsize=(10, 6))
plt.plot(gains, totalSignalPower, 'o-', label='Total Signal Power')
plt.xlabel('Gain')
plt.ylabel('signal Power')
plt.title('Signal Power as a Function of Gain')
plt.legend()
plt.grid(True)
plt.show()
print(totalSignalPower)

plt.figure(figsize=(10, 6))
plt.plot(gains, totalNoisePower, 'o-', label='Total Noise Power')
plt.xlabel('Gain')
plt.ylabel('noise power')
plt.title(' Noise Power as a Function of Gain')
plt.legend()
plt.grid(True)
plt.show()
print(totalNoisePower)

plt.figure(figsize=(10, 6))
plt.plot(gains, offsets, 'o-', label='Offset Evolution')
plt.xlabel('Gain')
plt.ylabel('Offset Value')
plt.title('Offset Evolution with Gain')
plt.legend()
plt.grid(True)
plt.show()
