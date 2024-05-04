import numpy as np
import matplotlib.pyplot as plt

# Function to normalize data
def normalize(data):
    return (data - np.min(data)) / (np.max(data) - np.min(data))

# Load data from a text file (replace with your file path)
data_path = '/Users/salmaessawab/Downloads/SFG spectrum OceanOptics.txt'  # Update to your actual file path
wavelengths, intensities = np.loadtxt(data_path, unpack=True)

# Specify the range of wavelengths you want to consider for the plot
start_wavelength = 600  # update this value
end_wavelength = 700    # update this value

# Mask to select the range of wavelengths
mask = (wavelengths >= start_wavelength) & (wavelengths <= end_wavelength)
selected_wavelengths = wavelengths[mask]
selected_intensities = intensities[mask]

# Normalize the selected intensities
normalized_intensities = normalize(selected_intensities)

# Plot the selected and normalized data
plt.figure(figsize=(10, 6))
plt.plot(selected_wavelengths, normalized_intensities, 'b-', label='Normalized Data')
plt.xlabel('Wavelength (nm)')
plt.ylabel('Normalized Intensity')
plt.title('OPA spectrum at 650nm with commercial spectrometer')
plt.legend()
plt.show()
