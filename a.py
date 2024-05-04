import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# Define a function to read and process the spectrum data
def read_spectrum(file_path, lambda0, dispersion_factor):
    # Load the spectrum data from the file
    spectrum_data = pd.read_csv(file_path, header=None, sep='\t')
    energy = spectrum_data[0]  # Assuming the first column is the energy/intensity data

    # Calculate the wavelength for each pixel position
    pixels = np.arange(len(energy))
    wavelengths = lambda0 - (pixels - (len(pixels) / 2)) * dispersion_factor

    return wavelengths, energy

# Function for plotting multiple spectra on one plot
def plot_multiple_spectra(file_paths, lambda0, dispersion_factor):
    plt.figure(figsize=(10, 6))

    # Plot each spectrum on the same axes and use the filename to get the wavelength
    for file_path in file_paths:
        # Extract the wavelength from the filename
        basename = os.path.basename(file_path)
        wavelength_label = basename.split('_')[1].split('.')[0] + ' nm'  # Assumes the format is SFG_<wavelength>.txt

        wavelengths, energy = read_spectrum(file_path, lambda0, dispersion_factor)
        plt.plot(wavelengths, energy, label=f'Spectrum at {wavelength_label}')

    plt.xlabel('Wavelength (nm)')
    plt.ylabel('Intensity')
    plt.title('Multiple Spectra')
    plt.grid(True)
    plt.legend()
    plt.show()

# Replace with your actual lambda0 value and dispersion factor
lambda0 = 669.7  # Center wavelength in nm
dispersion_factor = 0.0884700560287823  # Dispersion factor from pixels to nm

# List of file paths to your spectrum data files
file_paths = [
    '/Users/salmaessawab/Downloads/BSc project 2023/wavelength calibration/SFG_620.txt',
    '/Users/salmaessawab/Downloads/BSc project 2023/wavelength calibration/SFG_630.txt',
    '/Users/salmaessawab/Downloads/BSc project 2023/wavelength calibration/SFG_640.txt',
    '/Users/salmaessawab/Downloads/BSc project 2023/wavelength calibration/SFG_650.txt',
    '/Users/salmaessawab/Downloads/BSc project 2023/wavelength calibration/SFG_660.txt',
    '/Users/salmaessawab/Downloads/BSc project 2023/wavelength calibration/SFG_670.txt',
    '/Users/salmaessawab/Downloads/BSc project 2023/wavelength calibration/SFG_680.txt',
    '/Users/salmaessawab/Downloads/BSc project 2023/wavelength calibration/SFG_690.txt',
]

plot_multiple_spectra(file_paths, lambda0, dispersion_factor)
