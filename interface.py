import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import subprocess
from mittag_leffler import solve_ml_for_alpha
import periodictable as pt 
import traceback
import logging
from pathlib import Path

Path("beam-counts").mkdir(parents=True, exist_ok=True)

COUNTS_DIR="beam-counts/"
BEAM_COUNT=10000
ALL_OUTS={}
LNOFANHALF=np.log(0.5)
RESULTCSV="result.csv"
EXPERIMENTAL_DATA=pd.read_csv("conner1970.csv", sep=";", index_col=0)

element_names = list(EXPERIMENTAL_DATA.index)
beam_energies = list(EXPERIMENTAL_DATA.columns)[2:]

# element_names = ["zinc"]
# beam_energies = ["279.12"]

element_properties = {}
for el in pt.elements:
  element_properties[el.name] = el
for el_name in element_names:
  el = element_properties[el_name]

def linear(x, Mu):
  return Mu * x

# Acquire the simulation data for all elements/energies
if False:
  for element_name in element_names:
    EL=element_properties[element_name]
    ALL_OUTS[EL.symbol]={}
    df=None
    print("sim:", EL.name)

    for beam_energy in beam_energies:
      min_thickness = EXPERIMENTAL_DATA["min"][EL.name]
      max_thickness = EXPERIMENTAL_DATA["max"][EL.name]
      try:
        subprocess.run([
          "./gammaAttenuation",
          "G4_" + EL.symbol,
          beam_energy, "keV",
          str(BEAM_COUNT),
          "40",  # measurement count 
          str(min_thickness),
          str(max_thickness)
        ], capture_output=True)
        beam_counts = pd.read_csv(RESULTCSV, sep=";", index_col=0)
        beam_counts.columns = [beam_energy]
        if df is None:
          df = beam_counts
        else:
          df = df.join(beam_counts)
      except:
        print("error while running sim:", element_name, beam_energy)
        logging.error(traceback.format_exc()) 

    try:
      df.to_csv(COUNTS_DIR + EL.name + ".csv", sep = ";")
    except:
      print("error while writing sim results to file:", element_name, beam_energy)
      logging.error(traceback.format_exc()) 

for element_name in element_names:
  EL=element_properties[element_name]
  ALL_OUTS[EL.symbol] = {}

  for beam_energy in beam_energies:
    try:
      exp_Mu = EXPERIMENTAL_DATA[beam_energy][EL.name]
      sim_data = pd.read_csv(COUNTS_DIR + EL.name + ".csv", sep=";", index_col=0)[beam_energy]
      sim_linear_data = -np.log(sim_data[sim_data > 0]/BEAM_COUNT)
      [sim_Mu] = curve_fit(linear, sim_linear_data.index.values, sim_linear_data.values)[0]
      sim_HVL = -LNOFANHALF/sim_Mu

      # calculate alpha
      Mux = exp_Mu * sim_HVL * EL.density
      alpha = solve_ml_for_alpha(0.5, Mux)

      ALL_OUTS[EL.symbol][beam_energy] = {
        "alpha": alpha
      }
    except:
      print("error on:", element_name, beam_energy)
      logging.error(traceback.format_exc())

# for element_name in element_names:
#   EL=element_properties[element_name]
#   ALL_OUTS[EL.symbol] = {}
#   for beam_energy in beam_energies:
#     try:
#       OUT={"exp_Mu": EXPERIMENTAL_DATA[beam_energy]["aluminum"]}
#       ALL_OUTS[EL.symbol][beam_energy] = OUT
#       OUT["sim_data"] = pd.read_csv(RESULTCSV, sep=";", index_col=0)
#       data = OUT["sim_data"].copy()
#       OUT["sim_linear_data "] = data
#       data["count"] = -np.log(data["count"]/BEAM_COUNT)
#       [Mu] = curve_fit(linear, data.index.values, data["count"].values)[0]
#       OUT["sim_HVL"] = -LNOFANHALF/Mu
#       OUT["sim_Mu"] = Mu
#       Mux = OUT["exp_Mu"] * OUT["sim_HVL"] * EL.density
#       OUT["alpha"] = solve_ml_for_alpha(0.5, Mux)
#     except:
#       print("error on:", element_name, beam_energy)
#       logging.error(traceback.format_exc())

#def linear_attenuation_function(x):
#  return linear(x, Mu)

#def exp_curve(x, Mu, I0):
#  return I0 * np.exp(-Mu*x)
#delta_x = 0.01
#x = np.arange(0, MAX_THICKNESS + delta_x, delta_x)
#y = linear_attenuation_function(x)
#plt.plot(x, y)

#print("hvl:", hvl, "cm", ("(" + str(hvl*EL.density) + " g/cm2)") if EL.density else "")
#print("Mu:", Mu, "cm-1", ("(" + str(Mu/EL.density) + " cm2/g)") if EL.density else "")
#plot = plt.show()

#plt.plot(OUT.sim_data, linestyle="none", marker="o", markersize=8)
#[Mu2, I02] = curve_fit(
#  exp_curve,
#  OUT.sim_data.index.values,
#  OUT.sim_data["count"].values,
#  bounds=((0, 0), (600/MAX_THICKNESS, BEAM_COUNT))
#)[0]

#def attenuation_function(x):
#  return exp_curve(x, Mu2, I02)

#delta_x = 0.01
#x = np.arange(0, MAX_THICKNESS + delta_x, delta_x)
#y = attenuation_function(x)
#plt.plot(x, y)

#hvl2 = -LNOFANHALF/Mu2
# for R^2: https://stackoverflow.com/a/37899817
#print("HVL2:", hvl2, "cm", ("(" + str(hvl2*EL.density) + " g/cm2)") if EL.density else "")
#print("Mu2:", Mu2, "cm-1", ("(" + str(Mu2/EL.density) + " cm2/g)") if EL.density else "")
#print("I02 (calculated):", I02)
#plt.show()
