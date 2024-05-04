import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Define the Gaussian function
def gaussian(x, amplitude, mean, stddev):
    return amplitude * np.exp(-((x - mean) ** 2) / (2 * stddev ** 2))

# Define a function to read and process the spectrum data
def read_spectrum(file_path, lambda0):
    # Load the spectrum data from the file
    spectrum_data = pd.read_csv(file_path, header=None, sep='\t')
    energy = spectrum_data[0]

    # Calculate the wavelength for each pixel position
    pixels = np.arange(len(energy))
    wavelengths = lambda0 + (pixels - (len(pixels)-1) // 2) *(-0.0884)

    return wavelengths, energy

# Function to fit a Gaussian to the spectrum data
def fit_gaussian(wavelengths, intensities):
    try:
        # Guess initial parameters for Gaussian fit [amplitude, mean (peak), stddev]
        initial_guess = [max(intensities), wavelengths[np.argmax(intensities)], np.std(wavelengths)]
        popt, _ = curve_fit(gaussian, wavelengths, intensities, p0=initial_guess)
        return popt
    except RuntimeError as e:
        print(f"Error fitting Gaussian: {e}")
        return None

# Function to calculate FWHM from standard deviation
def calculate_fwhm(stddev):
    return 2 * np.sqrt(2 * np.log(2)) * stddev

# Function for calculating the resolution
def calculate_resolution(center_wavelength, fwhm):
    return center_wavelength / fwhm

# Function for plotting the spectrum and the Gaussian fit
def plot_spectrum_with_gaussian_fit(file_path, lambda0):
    wavelengths, energy = read_spectrum(file_path, lambda0)

    # Perform the Gaussian fit on the full range of data
    fitted_params = fit_gaussian(wavelengths, energy)
    if fitted_params is not None:
        amplitude, mean, stddev = fitted_params
        fwhm = calculate_fwhm(stddev)


        plt.figure(figsize=(10, 6))
        plt.plot(wavelengths, energy, 'b-', label=' Spectrum')
        '''plt.plot(wavelengths, gaussian(wavelengths, *fitted_params) / np.max(energy), 'r--', label='Gaussian Fit')'''
        plt.xlabel('Wavelength (nm)')
        plt.ylabel('Intensity')
        plt.title(f'Spectrum')
        plt.legend()
        plt.grid(True)
        plt.show()

        print(f"Gaussian Fit Parameters: Amplitude: {amplitude}, Mean (Center Wavelength): {mean}, Standard Deviation (Width): {stddev}")
        print(f"Calculated FWHM: {fwhm} nm")

        return fitted_params, fwhm
    else:
        print("Gaussian fitting was unsuccessful.")
        return None, None, None

# Replace with your actual lambda0 value and file path
lambda0 = 630
file_path = '/Users/salmaessawab/Downloads/BSc project 2023/wavelength calibration/SFG_630.txt'
gaussian_params, fwhm = plot_spectrum_with_gaussian_fit(file_path, lambda0)
