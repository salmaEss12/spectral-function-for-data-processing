import pandas as pd
import matplotlib.pyplot as plt
import os

def plot_spectrum(file_path, start_pixel=None, end_pixel=None):


    # Read the spectrum data from a file
    spectrum_data = pd.read_csv(file_path, header=None, sep='\t')
    intensity = spectrum_data[0]  # Assuming the intensity is in the first column (index 0)

    # Determine the pixel range for plotting
    if start_pixel is None:
        start_pixel = 0
    if end_pixel is None or end_pixel > len(intensity):
        end_pixel = len(intensity)

    # Slice the intensity data to the specified range
    pixel_range = range(start_pixel, end_pixel)
    intensity_range = intensity.iloc[start_pixel:end_pixel]
    range_length = end_pixel - start_pixel

    # Plot the spectrum
    plt.figure(figsize=(10, 6))
    plt.plot(pixel_range, intensity_range, label='Spectrum Intensity')
    plt.xlabel('Pixel Number')
    plt.ylabel('Intensity')
    plt.title(f'Spectrum Intensity from Pixel {start_pixel} to {end_pixel}')
    plt.legend()
    plt.grid(True)
    plt.show()

# Your script should specify these values correctly
start_pixel = 711
end_pixel = 730
file_path = '/Users/salmaessawab/Downloads/BSc project 2023/SN gain 2/SNgain0.txt'

# Call the function with the file path, output directory, and pixel range
plot_spectrum(file_path, start_pixel, end_pixel)
