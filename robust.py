import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from os import listdir
from os.path import isfile, join

# Define a function to read and process the spectrum data
def read_spectrum(file_path, lambda0, dispersion_factor):
    # Load the spectrum data from the file
    spectrum_data = pd.read_csv(file_path, header=None, sep='\t')
    energy = spectrum_data[0]  # Assuming the second column is intensity data

    # Calculate the wavelength for each pixel position
    pixels = np.arange(len(energy))
    wavelengths = lambda0 - (pixels - (len(pixels) / 2)) * dispersion_factor

    return wavelengths, energy

# Find the wavelength corresponding to the maximum intensity
def find_peak_wavelength(file_path, lambda0, dispersion_factor):
    wavelengths, energy = read_spectrum(file_path, lambda0, dispersion_factor)
    max_intensity_index = np.argmax(energy)
    peak_wavelength = wavelengths[max_intensity_index]
    return peak_wavelength

# Analyze the spectrometer's robustness
def analyze_spectrometer_robustness(directory, lambda0, dispersion_factor):
    file_paths = [f for f in listdir(directory) if isfile(join(directory, f)) and f.endswith('.txt')]

    peak_wavelengths = []
    for file_path in file_paths:
        full_path = join(directory, file_path)
        peak_wavelength = find_peak_wavelength(full_path, lambda0, dispersion_factor)
        peak_wavelengths.append(peak_wavelength)

    std_dev = np.std(peak_wavelengths)
    return peak_wavelengths, std_dev

# Function to plot the peak wavelengths
def plot_peak_wavelengths(peak_wavelengths):
    plt.figure(figsize=(10, 6))
    plt.plot(peak_wavelengths, marker='o', linestyle='', color='blue', label='Peak Wavelength')
    mean_wavelength = np.mean(peak_wavelengths)
    plt.axhline(y=mean_wavelength, color='r', linestyle='-', label=f'Mean Wavelength: {mean_wavelength:.2f} nm')
    plt.xlabel('Spectrum File Index')
    plt.ylabel('Wavelength (nm)')
    plt.title('Peak Wavelengths Across Multiple Spectra')
    plt.legend()
    plt.grid(True)
    plt.show()

# Plotting the histogram of peak wavelengths
def plot_histogram_peak_wavelengths(peak_wavelengths):
    plt.figure(figsize=(10, 6))
    plt.hist(peak_wavelengths, bins='auto', color='blue', alpha=0.7, rwidth=0.85)
    plt.xlabel('Wavelength (nm)')
    plt.ylabel('Frequency')
    plt.title('Distribution of Peak Wavelengths')
    plt.grid(axis='y', alpha=0.75)
    plt.show()

# Example usage
directory = '/Users/salmaessawab/Downloads/robustness 2'  # Update this to your files' location
lambda0 = 632.8  # Update this to your expected center wavelength
dispersion_factor = 0.0884  # Adjust based on your calibration data
peak_wavelengths, std_dev = analyze_spectrometer_robustness(directory, lambda0, dispersion_factor)

print("Peak Wavelengths:", peak_wavelengths)
print("Standard Deviation of Peak Wavelength Displacement:", std_dev)

# Plotting the results
plot_peak_wavelengths(peak_wavelengths)
plot_histogram_peak_wavelengths(peak_wavelengths)
