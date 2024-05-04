import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

def read_spectrum(file_path):
    spectrum_data = pd.read_csv(file_path, header=None, sep='\t')
    energy = spectrum_data[0]
    return energy

def gaussian(x, mean, amplitude, standard_deviation):
    return amplitude * np.exp(- (x - mean)**2 / (2 * standard_deviation**2))

def fit_and_plot_gaussian(noise_data, xmin=None, xmax=None):
    # Prepare the histogram data
    bin_heights, bin_borders, _ = plt.hist(noise_data, bins=30, label='Noise Data', alpha=0.6, color='b', density=True)
    bin_centers = bin_borders[:-1] + np.diff(bin_borders) / 2

    # Fit the Gaussian function to the histogram data
    popt, _ = curve_fit(gaussian, bin_centers, bin_heights, p0=[np.mean(noise_data), np.max(bin_heights), np.std(noise_data)])

    # Generate enough x values to make the curves smooth
    x_interval_for_fit = np.linspace(bin_borders[0], bin_borders[-1], 10000)

    # Plot the fitted Gaussian curve
    plt.plot(x_interval_for_fit, gaussian(x_interval_for_fit, *popt), label='Fitted Gaussian', color='r')
    plt.xlabel('Noise Value')
    plt.ylabel('Density')
    plt.legend()

    # Show standard deviation on the plot
    plt.title(f'Gaussian Fit: Mean = {popt[0]:.2f}, Std Dev = {popt[2]:.2f}')

    # Set the x-axis limits if specified
    if xmin is not None and xmax is not None:
        plt.xlim([xmin, xmax])

    plt.show()

    return popt[2]  # Return the fitted standard deviation

# Example usage
file_path = '/Users/salmaessawab/Downloads/BSc project 2023/SN gain 2/noise32.txt'  # Replace with your actual file path
energy = read_spectrum(file_path)

# Set your desired x-axis limits here
xmin, xmax = 0, 200
fitted_std_dev = fit_and_plot_gaussian(energy, xmin, xmax)
print(f"Fitted Standard Deviation: {fitted_std_dev:.2f}")
