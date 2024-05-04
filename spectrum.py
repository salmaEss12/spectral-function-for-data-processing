import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Define the Gaussian function with an offset
def gaussian_with_offset(x, amplitude, mean, stddev, offset):
    return amplitude * np.exp(-((x - mean) ** 2) / (2 * stddev ** 2)) + offset

# Define a function to read and process the spectrum data
def read_spectrum(file_path, lambda0, dispersion_factor):
    # Load the spectrum data from the file
    spectrum_data = pd.read_csv(file_path, header=None, sep='\t')
    energy = spectrum_data[0]  # Make sure this column index matches the energy data

    # Calculate the wavelength for each pixel position
    pixels = np.arange(len(energy))
    wavelengths = lambda0 - (pixels - (len(pixels) / 2)) * dispersion_factor

    return wavelengths, energy

# Function to fit a Gaussian with offset to the spectrum data
def fit_gaussian_with_offset(wavelengths, intensities):
    try:
        # Guess initial parameters for Gaussian with offset fit [amplitude, mean, stddev, offset]
        initial_guess = [max(intensities), wavelengths[np.argmax(intensities)], 10, min(intensities)]
        popt, _ = curve_fit(gaussian_with_offset, wavelengths, intensities, p0=initial_guess)
        return popt
    except RuntimeError as e:
        print(f"Error fitting Gaussian with offset: {e}")
        return None

# Function to calculate FWHM from standard deviation
def calculate_fwhm(stddev):
    return 2 * np.sqrt(2 * np.log(2)) * stddev

# Function for plotting the spectrum and the Gaussian fit with offset
def plot_spectrum_with_gaussian_fit(file_path, lambda0, dispersion_factor):
    wavelengths, energy = read_spectrum(file_path, lambda0, dispersion_factor)

    # Normalize the spectrum data
    normalized_energy = energy / np.max(energy)

    # Perform the Gaussian with offset fit on the normalized data
    fitted_params = fit_gaussian_with_offset(wavelengths, normalized_energy)
    if fitted_params is not None:
        amplitude, mean, stddev, offset = fitted_params
        fwhm = calculate_fwhm(stddev)

        # Generate Gaussian fit data and normalize it
        gaussian_fit = gaussian_with_offset(wavelengths, *fitted_params)
        normalized_gaussian_fit = gaussian_fit / np.max(gaussian_fit)

        # Plot the normalized spectrum and the normalized Gaussian fit with offset
        plt.figure(figsize=(10, 6))
        plt.plot(wavelengths, normalized_energy, 'b-', label='Normalized Spectrum')
        plt.plot(wavelengths, normalized_gaussian_fit, 'r--', label='Normalized Gaussian Fit with Offset')
        plt.xlabel('Wavelength (nm)')
        plt.ylabel('Normalized Intensity')
        plt.title('HeNe Spectrum using our spectrometer Flame)')

        # Annotate the FWHM on the graph
        plt.annotate(f'Resolution: {fwhm:.2f} nm', xy=(0.05, 0.95), xycoords='axes fraction',
                     fontsize=10, horizontalalignment='left', verticalalignment='top',
                     bbox=dict(boxstyle="round", facecolor='white', alpha=0.5))

        plt.legend()
        plt.xlim(min(wavelengths), max(wavelengths))  # Set to the range of your wavelengths
        plt.grid(True)
        plt.show()

        print(f"Gaussian Fit with Offset Parameters: Amplitude: {amplitude}, Mean (Center Wavelength): {mean}, Standard Deviation (Width): {stddev}, Offset: {offset}")
        print(f"Calculated FWHM: {fwhm:.2f} nm")

        return fitted_params, fwhm
    else:
        print("Gaussian fitting with offset was unsuccessful.")
        return None, None

# Replace with your actual lambda0 value and file path
lambda0 = 632.8  # Update this value to the expected center wavelength
dispersion_factor = 0.0884  # This value should be obtained from your calibration data
file_path = '/Users/salmaessawab/Downloads/BSc project 2023/gratings_resolution/HeNe_GR600_S1.txt'  # Update this to the path of your data file
gaussian_params, fwhm = plot_spectrum_with_gaussian_fit(file_path, lambda0, dispersion_factor)
