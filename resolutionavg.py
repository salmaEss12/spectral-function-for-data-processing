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
    wavelengths = lambda0 + (pixels - (len(pixels)-1) // 2) * (-0.0884)

    return wavelengths, energy

# Function to fit a Gaussian to the spectrum data and return parameters and their errors
def fit_gaussian(wavelengths, intensities):
    try:
        # More sophisticated initial parameter estimation
        mean_estimate = wavelengths[np.argmax(intensities)]
        amplitude_estimate = np.max(intensities)
        half_max = amplitude_estimate / 2
        closest_half_max_idx = np.argmin(np.abs(intensities - half_max))
        stddev_estimate = np.abs(mean_estimate - wavelengths[closest_half_max_idx]) / np.sqrt(2 * np.log(2))

        initial_guess = [amplitude_estimate, mean_estimate, stddev_estimate]

        popt, pcov = curve_fit(gaussian, wavelengths, intensities, p0=initial_guess)
        perr = np.sqrt(np.diag(pcov))  # Standard deviations of parameters
        return popt, perr
    except RuntimeError as e:
        print(f"Error fitting Gaussian: {e}")
        return None, None

def calculate_fwhm(stddev):
    return 2 * np.sqrt(2 * np.log(2)) * stddev

# Function to plot the spectrum and the Gaussian fit with error representation
def plot_spectrum_with_gaussian_fit(file_path, lambda0):
    wavelengths, energy = read_spectrum(file_path, lambda0)
    plt.figure(figsize=(10, 6))

    # Perform Gaussian fit
    fitted_params, perr = fit_gaussian(wavelengths, energy)
    if fitted_params is not None and perr is not None:
        amplitude, mean, stddev = fitted_params
        fwhm = calculate_fwhm(stddev)
        plt.plot(wavelengths, energy, 'b-', label='Spectrum')

        # Plot the fitted Gaussian curve over the full range
        fitted_curve = gaussian(wavelengths, *fitted_params)
        plt.plot(wavelengths, fitted_curve, 'r--', label='Gaussian fit')

        # Plot the standard deviation/error as a shaded area
        sigma = np.linspace(-2 * stddev, 2 * stddev, 100)
        sigma_wavelengths = mean + sigma
        sigma_curve = gaussian(sigma_wavelengths, amplitude, mean, stddev)
        plt.fill_between(sigma_wavelengths, sigma_curve - perr[0], sigma_curve + perr[0], color='red', alpha=0.2, label='Fit Error')

        plt.xlabel('Wavelength (nm)')
        plt.ylabel('Intensity')
        plt.title('Spectrum of HeNe ')
        plt.legend()
        plt.grid(True)
        plt.show()
    else:
        print(f"Could not calculate FWHM for {file_path}.")
        fwhm = None

    return fwhm

# Function to process a list of files and calculate FWHM values
def process_files(file_paths, lambda0):
    fwhm_values = []
    for file_path in file_paths:
        fwhm = plot_spectrum_with_gaussian_fit(file_path, lambda0)
        print(fwhm)
        if fwhm is not None:
            fwhm_values.append(fwhm)

    # Calculate and display the sum and average of the FWHM values
    if fwhm_values:
        sum_fwhm = np.sum(fwhm_values)
        avg_fwhm = np.mean(fwhm_values)
        print(f"Sum of FWHM values: {sum_fwhm} nm")
        print(f"Average FWHM: {avg_fwhm} nm")
    else:
        print("No FWHM values to sum and average.")

# Example usage with placeholder file paths
lambda0 = 632.8  # Replace with your actual central wavelength
file_paths = [
    '/Users/salmaessawab/Downloads/BSc project 2023/gratings_resolution/HeNe_GR600_C1.txt',
    '/Users/salmaessawab/Downloads/BSc project 2023/gratings_resolution/HeNe_GR600_C2.txt',
    '/Users/salmaessawab/Downloads/BSc project 2023/gratings_resolution/HeNe_GR600_S1.txt',
    '/Users/salmaessawab/Downloads/BSc project 2023/gratings_resolution/HeNe_GR600_S2.txt',
    '/Users/salmaessawab/Downloads/BSc project 2023/gratings_resolution/HeNe_GR600_F1.txt',
    '/Users/salmaessawab/Downloads/BSc project 2023/gratings_resolution/HeNe_GR600_F2.txt'
]
process_files(file_paths, lambda0)
