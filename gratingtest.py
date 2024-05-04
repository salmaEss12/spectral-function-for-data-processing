import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from os.path import isfile

# Define the Gaussian function
def gaussian(x, amplitude, mean, stddev):
    return amplitude * np.exp(-((x - mean) ** 2) / (2 * stddev ** 2))

# Define a function to read and process the spectrum data, adjusting D based on grating
def read_spectrum(file_path, lambda0):
    # Determine the grating value from the filename and set D accordingly
    if "600" in file_path:
        D = 0.075
    elif "1200" in file_path:
        D = 0.0368
    elif "1800" in file_path:
        D = 0.0244
    else:
        D = 0.0884  # Default value or handle as error

    # Load the spectrum data from the file, assuming tab-separated values
    spectrum_data = pd.read_csv(file_path, header=None, sep='\t')
    energy = spectrum_data[0]

    # Normalize the intensity so that the maximum is 1
    energy /= np.max(energy)

    # Calculate the wavelength for each pixel position
    pixels = np.arange(len(energy))
    wavelengths = lambda0 + (pixels - (len(pixels)-1) // 2) * (D)

    return wavelengths, energy

# Function to fit a Gaussian to the spectrum data
def fit_gaussian(wavelengths, intensities):
    # Narrow down the data to the peak for better fitting
    # Assume the peak is the highest point in the data
    peak_region = intensities > (0.5 * np.max(intensities))
    wavelengths_peak = wavelengths[peak_region]
    intensities_peak = intensities[peak_region]

    try:
        # Guess initial parameters for Gaussian fit [amplitude, mean (peak), stddev]
        initial_guess = [np.max(intensities_peak), wavelengths_peak[np.argmax(intensities_peak)], np.std(wavelengths_peak)]
        popt, _ = curve_fit(gaussian, wavelengths_peak, intensities_peak, p0=initial_guess)
        return popt
    except RuntimeError as e:
        print(f"Error fitting Gaussian: {e}")
        return None

# Function to calculate FWHM from standard deviation
def calculate_fwhm(stddev):
    return 2 * np.sqrt(2 * np.log(2)) * abs(stddev)

# Assuming lambda0 is known and the same for all files
lambda0 = 632.8  # Replace with your actual lambda0 value

# Manually enter the file paths
file_paths = [
    "/Users/salmaessawab/Desktop/a/HeNe_GR600.txt",
    "/Users/salmaessawab/Desktop/a/HeNe_GR1200.txt",
    "/Users/salmaessawab/Desktop/a/HeNe_GR1800.txt"
]

# Plot the spectrum for each file and fit a Gaussian
plt.figure(figsize=(10, 6))

for file_path in file_paths:
    if isfile(file_path):
        # Extract the part of the filename without the path and extension
        grating_info = file_path.split('/')[-1].split('.txt')[0]

        # Read and process the spectrum file
        wavelengths, normalized_intensities = read_spectrum(file_path, lambda0)

        # Fit a Gaussian to the spectrum
        fitted_params = fit_gaussian(wavelengths, normalized_intensities)
        if fitted_params is not None:
            # Calculate the FWHM
            fwhm = calculate_fwhm(fitted_params[2])
            print(fwhm)

            # Plot the spectrum and the Gaussian fit
            plt.plot(wavelengths, normalized_intensities, label=f'{grating_info} (Intensity Normalized)')
            plt.plot(wavelengths, gaussian(wavelengths, *fitted_params), 'r--', linewidth=1.5, label=f'{grating_info} Fit (FWHM: {fwhm:.2f} nm)')

    else:
        print(f"File {file_path} is missing.")

# Set the x-axis to the desired wavelength range
plt.xlim(632, 634)

# Finalize the plot
plt.xlabel('Wavelength (nm)')
plt.ylabel('Normalized Intensity')
plt.title('Spectra and Gaussian Fits for Different Gratings (Normalized)')
plt.legend()
plt.grid(True)
plt.show()
