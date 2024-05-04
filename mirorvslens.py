import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def read_spectrum(file_path):
    """Read spectrum data from a file without converting to wavelengths."""
    try:
        spectrum_data = pd.read_csv(file_path, header=None, sep='\t')
        energy = spectrum_data[0]
        pixels = np.arange(len(energy))
        return pixels, energy
    except Exception as e:
        print(f"Error reading spectrum data: {e}")
        return None, None

def plot_spectra_normalized_and_aligned(file_path1, file_path2):
    """Plot normalized and aligned spectra for two files, based on pixel numbers."""
    pixels1, energy1 = read_spectrum(file_path1)
    pixels2, energy2 = read_spectrum(file_path2)

    if pixels1 is None or pixels2 is None:
        print("Error in reading spectra.")
        return

    # Find the peak pixel number for both spectra
    peak_pixel_1 = pixels1[np.argmax(energy1)]
    peak_pixel_2 = pixels2[np.argmax(energy2)]

    # Shift the pixel numbers to align the peaks
    shift_pixels2 = peak_pixel_1 - peak_pixel_2
    pixels2_shifted = pixels2 + shift_pixels2

    # Normalize spectra by the max of the first spectrum for plotting
    max_intensity_1 = np.max(energy1)
    max_intensity_2 = np.max(energy2)
    normalized_energy1 = energy1 / max_intensity_1
    normalized_energy2 = energy2 / max_intensity_1

    plt.figure(figsize=(10, 6))
    plt.plot(pixels1, normalized_energy1, 'b-', label='Spectrum 1 - Focusing Lens')
    plt.plot(pixels2_shifted, normalized_energy2, 'g-', label='Spectrum 2 - Parabolic Mirror')

    # Set the x-axis limits to focus on pixels between 600 and 700
    plt.xlim(500, 700)

    plt.xlabel('Pixel Number')
    plt.ylabel('Normalized Intensity')
    plt.title('Efficiency performace comparaison of Parabolic mirror and Focusing lense')
    plt.legend()
    plt.grid(True)
    plt.show()

# Example usage with placeholders for actual file paths for your spectra
file_path1 = '/Users/salmaessawab/Downloads/BSc project 2023/lens vs parabolic mirror/final measures/finallense.txt'  # Update with actual file path
file_path2 = '/Users/salmaessawab/Downloads/BSc project 2023/lens vs parabolic mirror/final measures/paramirrorfinal2.txt'  # Update with actual file path

try:
    plot_spectra_normalized_and_aligned(file_path1, file_path2)
except Exception as e:
    print(f"An unexpected error occurred: {e}")
