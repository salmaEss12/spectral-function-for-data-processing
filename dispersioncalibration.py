import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

file_paths = [
    "/Users/salmaessawab/Downloads/wavelength calibration/SFG_620.txt",
    "/Users/salmaessawab/Downloads/wavelength calibration/SFG_630.txt",
    "/Users/salmaessawab/Downloads/wavelength calibration/SFG_640.txt",
    "/Users/salmaessawab/Downloads/wavelength calibration/SFG_650.txt",
    "/Users/salmaessawab/Downloads/wavelength calibration/SFG_660.txt",
    "/Users/salmaessawab/Downloads/wavelength calibration/SFG_670.txt"
]
wavelengths = [620, 630, 640, 650, 660, 670]  # Update this list according to your file_paths


def find_peak_pixel_position(file_path):
    data = pd.read_csv(file_path, header=None, sep='\t')
    peak_pixel_position = np.argmax(data[0])
    return peak_pixel_position


peak_pixel_positions = [find_peak_pixel_position(path) for path in file_paths]


plt.figure(figsize=(10, 6))
plt.plot(peak_pixel_positions, wavelengths, 'o-', label='Pixel Position vs. Wavelength')
plt.xlabel('Pixel Position')
plt.ylabel('Wavelength (nm)')
plt.title('Pixel Position vs. Wavelength')
plt.legend()
plt.grid(True)
plt.show()


slope, intercept = np.polyfit(peak_pixel_positions, wavelengths, 1)


x_line = np.array(peak_pixel_positions)
y_line = slope * x_line + intercept
plt.figure(figsize=(10, 6))
plt.plot(peak_pixel_positions, wavelengths, 'o', label='Measured Data of Pixel Position vs. Wavelength')
plt.plot(x_line, y_line, 'r-')
plt.xlabel('Pixel Position')
plt.ylabel('Wavelength (nm)')
plt.title('Linear Fit of Pixel Position to Wavelength')
plt.legend()
plt.grid(True)
plt.show()

print(f"Pixel-to-wavelength conversion factor (slope): {slope} nm/pixel")
