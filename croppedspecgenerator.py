import pandas as pd
import os

def save_cropped_spectrum(file_path, output_directory, start_pixel=None, end_pixel=None):
    # Make sure output directory exists
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Read the spectrum data from a file
    spectrum_data = pd.read_csv(file_path, header=None, sep='\t')
    intensity = spectrum_data[0]  # Assuming the intensity is in the first column (index 0)

    # Determine the pixel range for cropping
    if start_pixel is None:
        start_pixel = 0
    if end_pixel is None or end_pixel > len(intensity):
        end_pixel = len(intensity)

    # Crop the intensity data to the specified range
    intensity_cropped = intensity.iloc[start_pixel:end_pixel]

    # Save the cropped intensity data to a new file
    output_file_path = os.path.join(output_directory, os.path.basename(file_path))
    intensity_cropped.to_csv(output_file_path, index=False, header=False, sep='\t')

# Specify the input directory containing the spectrum text files
input_directory = '/Users/salmaessawab/Downloads/BSc project 2023/SN gain 2'

# Specify the output directory for the cropped files
output_directory = '/Users/salmaessawab/Desktop/SNRgain'

# Specify the start and end pixel for cropping
start_pixel = 711
end_pixel = 730

# Loop through each file in the input directory and process it
for file_name in os.listdir(input_directory):
    file_path = os.path.join(input_directory, file_name)
    if os.path.isfile(file_path):
        save_cropped_spectrum(file_path, output_directory, start_pixel, end_pixel)
