import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Define a function to read and process the spectrum data
def read_spectrum(file_path, lambda0, dispersion_factor):
    # Load the spectrum data from the file
    spectrum_data = pd.read_csv(file_path, header=None, sep='\t')
    energy = spectrum_data[0]  # Make sure this column index matches the intensity data

    # Calculate the wavelength for each pixel position
    pixels = np.arange(len(energy))
    wavelengths = lambda0 - (pixels - (len(pixels) / 2)) * dispersion_factor

    return wavelengths, energy

# Function for plotting the spectrum
def plot_spectrum(file_path, lambda0, dispersion_factor):
    wavelengths, energy = read_spectrum(file_path, lambda0, dispersion_factor)

    # Normalize the spectrum for plotting
    normalized_energy = energy / np.max(energy)

    # Plot the normalized spectrum
    plt.figure(figsize=(10, 6))
    plt.plot(wavelengths, normalized_energy, 'b-', label='Normalized Spectrum')
    plt.xlabel('Wavelength (nm)')
    plt.ylabel('Normalized Intensity')
    plt.title(f'OPA spectrum at 650nm_GAIN48_ND6')
    plt.legend()
    plt.grid(True)
    # Limit x-axis to 600-700 nm (if desired, otherwise remove or adjust these limits)
    # plt.xlim([600, 700])
    plt.show()

# Replace with your actual lambda0 value and file path
lambda0 = 670  # Update this value to the expected center wavelength
dispersion_factor = 0.0884  # This value should be obtained from your calibration data
file_path = '/Users/salmaessawab/Downloads/BSc project 2023/OPA/SFG650_10nW_ND60_exp1s_gain48dB.txt'  # Update this to the path of your data file

plot_spectrum(file_path, lambda0, dispersion_factor)
