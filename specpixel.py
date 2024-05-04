import pandas as pd
import matplotlib.pyplot as plt
import os

def plot_spectrum(file_path, output_directory, start_pixel=None, end_pixel=None):
    # Ensure the output directory exists
    os.makedirs(output_directory, exist_ok=True)

    # Read the spectrum data from a file
    spectrum_data = pd.read_csv(file_path, header=None, sep='\t')
    intensity = spectrum_data[0]  # Assuming the intensity is in the second column

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

    # Construct the output file path within the specified directory
    base_name = os.path.basename(file_path)  # Extracts the file name from the file path
    output_file_name = os.path.splitext(base_name)[0] + f'_{range_length}.txt'
    output_file_path = os.path.join(output_directory, output_file_name)

    # Save the range of pixels and their intensities to a new text file
    intensity_range.to_csv(output_file_path, index=False, header=False, sep='\t')
    print(f'Saved sliced spectrum to {output_file_path}')

# Specify the directory where you want to save the new files
output_directory = '/Users/salmaessawab/Desktop/snrpixel'

# Replace with the path to your spectrum file
start_pixel = 712
end_pixel = 730
file_path = '/Users/salmaessawab/Downloads/SNRvsbins/noise_exp1.01_gain0_bin8.txt'

# Call the function with the file path, output directory, and pixel range
plot_spectrum(file_path, output_directory, start_pixel, end_pixel)
