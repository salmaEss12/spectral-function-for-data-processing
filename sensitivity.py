import numpy as np

def calcul_sensitivity(power, lambda_):
    c = 3 * 10**8         # Speed of light in m/s
    h = 6.626 * 10**-34   # Planck's constant in J*s
    E = (h * c) / lambda_ # Energy of a photon
    N = power / E         # Number of photons per second
    return N

lambda_ = 632.8 * 10**-9 # Wavelength in meters
power = 35* 10**-9  # Power in watts
F=11
N=48/20
N = calcul_sensitivity(power, lambda_)/(10**(F))
print(f"{N:.3e}")
