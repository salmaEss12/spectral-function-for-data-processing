import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

# Define the functions as before, without modifications
def read_spectrum(file_paths, lambda0):
    sum_spectrum = None
    for file_path in file_paths:
        spectrum_data = pd.read_csv(file_path, header=None, sep='\t')
        energy = spectrum_data[0]
        if sum_spectrum is None:
            sum_spectrum = energy
        else:
            sum_spectrum += energy
    avg_spectrum = sum_spectrum / len(file_paths)
    pixels = np.arange(len(avg_spectrum))
    wavelengths = lambda0 + (pixels - (len(pixels)-1) // 2) * (-0.0884)
    return wavelengths, avg_spectrum

def read_professional_spectrum(file_path):
    spectrum_data = pd.read_csv(file_path, header=None, sep='\t')
    energy = spectrum_data[1]
    wavelengths = spectrum_data[0]
    return wavelengths, energy

def calibrate_spectrum(own_spectrum_paths, professional_spectrum_path, lambda0):
    own_wavelengths, own_intensities = read_spectrum(own_spectrum_paths, lambda0)
    professional_wavelengths, professional_intensities = read_professional_spectrum(professional_spectrum_path)
    interpolate_professional_intensities = interp1d(professional_wavelengths, professional_intensities,
                                                     kind='cubic', bounds_error=False, fill_value='extrapolate')
    matched_professional_intensities = interpolate_professional_intensities(own_wavelengths)
    calibration_factors = matched_professional_intensities / own_intensities
    return own_wavelengths, calibration_factors

# Assuming these paths are placeholders for demonstration purposes
own_spectrum_paths = [
    '/Users/salmaessawab/Downloads/intensitycalibration/wl_exp100ms_gain0_1.txt',
    '/Users/salmaessawab/Downloads/intensitycalibration/wl_exp100ms_gain0_2.txt',
    '/Users/salmaessawab/Downloads/intensitycalibration/wl_exp100ms_gain0_3.txt',
    '/Users/salmaessawab/Downloads/intensitycalibration/wl_exp100ms_gain0_4.txt',
    '/Users/salmaessawab/Downloads/intensitycalibration/wl_exp100ms_gain0_5.txt',
    '/Users/salmaessawab/Downloads/intensitycalibration/wl_exp100ms_gain0_6.txt',

]
professional_spectrum_path = '/Users/salmaessawab/Downloads/intensitycalibration/wlflame_2__0__13-36-26-985.txt'
lambda0 = 632.8

# Calibrate spectrum
wavelengths, calibration_factors = calibrate_spectrum(own_spectrum_paths, professional_spectrum_path, lambda0)

# Normalize the calibration factors
calibration_factors_normalized = calibration_factors / np.max(calibration_factors)

# Plotting
plt.figure(figsize=(10, 6))
plt.plot(wavelengths, calibration_factors_normalized, label='Normalized Calibration Factor', marker='o', linestyle='none')

# Polynomial fit on the normalized calibration factors
degree = 6
coefficients = np.polyfit(wavelengths, calibration_factors_normalized, degree)
polynomial = np.poly1d(coefficients)
x_poly = np.linspace(min(wavelengths), max(wavelengths), 100)
y_poly = polynomial(x_poly)
plt.plot(x_poly, y_poly, label=f'Polynomial Fit (Degree {degree})', linewidth=2)

plt.xlabel('Wavelength (nm)')
plt.ylabel('Normalized Intensity Calibration Factor')
plt.title('Intensity Calibration Curve with Polynomial Fit')
plt.legend()
plt.grid(True)
plt.show()
