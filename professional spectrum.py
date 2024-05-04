import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Define a Gaussian function
def gaussian(x, mean, amplitude, standard_deviation):
    return amplitude * np.exp(-((x - mean)**2 / (2 * standard_deviation**2)))

# Load data from a text file (replace 'path_to_your_data.txt' with your file path)
wavelengths, intensities = np.loadtxt('/Users/salmaessawab/Downloads/BSc project 2023/HeNespectroFlame_FLMT030061__1__09-38-34-162.txt', unpack=True)

# Select the range of 600 to 700 nm
mask = (wavelengths >= 600) & (wavelengths <= 700)
selected_wavelengths = wavelengths[mask]
selected_intensities = intensities[mask]

# Normalize the selected intensities
selected_intensities_normalized = selected_intensities / np.max(selected_intensities)

# Perform the Gaussian fit on the selected and normalized range
initial_guess = [650, 1, 10]  # Example initial guess, normalized amplitude
params, cov = curve_fit(gaussian, selected_wavelengths, selected_intensities_normalized, p0=initial_guess)

# Generate data from the fitted Gaussian curve
fitted_curve = gaussian(selected_wavelengths, *params)

# Normalize the fitted Gaussian curve
normalized_fitted_curve = fitted_curve / np.max(fitted_curve)

# Calculate the FWHM
fwhm = 2 * np.sqrt(2 * np.log(2)) * params[2]

# Plot the normalized original data and the normalized fitted Gaussian curve
plt.figure(figsize=(10, 6))
plt.plot(wavelengths, intensities / np.max(intensities), 'b.', label='Normalized Data')
plt.plot(selected_wavelengths, normalized_fitted_curve, 'r-', label='Normalized Gaussian Fit')
plt.xlabel('Wavelength (nm)')
plt.ylabel('Normalized Intensity')
plt.title('HeNe Spectrum using professional spectrometer Flame)')
plt.annotate(f'resolution : {fwhm:.2f} nm', xy=(0.05, 0.95), xycoords='axes fraction', fontsize=12,
             horizontalalignment='left', verticalalignment='top', bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="b", lw=2))
plt.xlim(600, 700)
plt.legend()
plt.show()

# Print out the FWHM result
print(f"The Full Width at Half Maximum (FWHM) is: {fwhm:.2f} nm")
