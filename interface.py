import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import subprocess
import os

LNOFANHALF=np.log(0.5)
RESULTCSV="result.csv"

def clear_result():
    if os.path.isfile(RESULTCSV):
        os.remove(RESULTCSV)

def exp_curve(x, Mu, I0):
    return I0 * np.exp(-Mu*x)

MATERIAL="G4_Fe"
BEAM_ENERGY_VALUE=200
BEAM_ENERGY_UNIT="MeV"
BEAM_COUNT=10000
MEASUREMENT_COUNT=20
MIN_THICKNESS=0
MAX_THICKNESS=2

clear_result()
subprocess.run([
    "./gammaAttenuation",
    MATERIAL,
    str(BEAM_ENERGY_VALUE),
    BEAM_ENERGY_UNIT,
    str(BEAM_COUNT),
    str(MEASUREMENT_COUNT),
    str(MIN_THICKNESS),
    str(MAX_THICKNESS)
], capture_output=True)

data = pd.read_csv("result.csv", sep=";", index_col=0)
clear_result()
plt.plot(data, linestyle="none", marker="o", markersize=8)
[Mu, I0] = curve_fit(exp_curve, data.index.values, data["count"].values)[0]

def attenuation_function(x):
    return exp_curve(x, Mu, I0)

delta_x = 0.01
x = np.arange(0, MAX_THICKNESS + delta_x, delta_x)
y = attenuation_function(x)

plt.plot(x, y)

# OUTPUT:
print("Material:", MATERIAL)
print("Gamma Energy:", BEAM_ENERGY_VALUE, BEAM_ENERGY_UNIT)
print("HVL:", -LNOFANHALF/Mu)
print("Mu:", Mu)
print("I0 (actual and from fitted curve):", BEAM_COUNT, "-", I0)
plt.show()
