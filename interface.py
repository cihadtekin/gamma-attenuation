import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import subprocess
from mittag_leffler import solve_ml_for_alpha, mittag_leffler, mittag_leffler_basic
import periodictable as pt 
import traceback
import logging
from pathlib import Path
from labellines import labelLine, labelLines
import os
from IPython.display import display, HTML

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

Path("beam-counts").mkdir(parents=True, exist_ok=True)

COUNTS_DIR="beam-counts/"
BEAM_COUNT=10000
OUT={}
LNOFANHALF=np.log(0.5)
RESULTCSV="result.csv"

EXPERIMENTAL_DATA=pd.read_csv("conner1970.csv", sep=";", index_col=0)
MIN_THICKNESS_DATA=pd.read_csv("min-thickness.csv", sep=";", index_col=0)
MAX_THICKNESS_DATA=pd.read_csv("max-thickness.csv", sep=";", index_col=0)

element_names = list(EXPERIMENTAL_DATA.index)
beam_energies = list(EXPERIMENTAL_DATA.columns)

# element_names = ["beryllium"]
# beam_energies = ["88.09"]

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
    print("sim:", element_name)
    dir = COUNTS_DIR + element_name + "/"
    Path(dir).mkdir(parents=True, exist_ok=True)

    for beam_energy in beam_energies:
      try:
        subprocess.run([
          "./gammaAttenuation",
          "G4_" + element_properties[element_name].symbol,
          beam_energy, "keV",
          str(BEAM_COUNT),
          "40",  # measurement count 
          str(MIN_THICKNESS_DATA[beam_energy][element_name]),
          str(MAX_THICKNESS_DATA[beam_energy][element_name])
        ], capture_output=True)
        os.rename(RESULTCSV, dir + beam_energy + ".csv")
      except:
        print("error while running sim:", element_name, beam_energy)
        logging.error(traceback.format_exc()) 

if True:
  for element_name in element_names:
    el=element_properties[element_name]
    ind=el.name + " (" + str(el.mass) + ")"
    OUT[ind] = {}

    for beam_energy in beam_energies:
      sim_file = COUNTS_DIR + el.name + "/" + beam_energy + ".csv"
      if not Path(sim_file).exists():
        continue

      try:
        exp_Mu = EXPERIMENTAL_DATA[beam_energy][el.name]
        sim_data = pd.read_csv(sim_file, sep=";", index_col=0)["count"]
        sim_linear_data = -np.log(sim_data[sim_data > 0]/BEAM_COUNT)
        [sim_Mu] = curve_fit(linear, sim_linear_data.index.values, sim_linear_data.values)[0]
        sim_HVL = -LNOFANHALF/sim_Mu

        # calculate alpha
        Mux = exp_Mu * sim_HVL * el.density
        alpha = solve_ml_for_alpha(0.5, Mux)

        OUT[ind][beam_energy] = {
          "sim_Mu": sim_Mu / el.density,
          "sim_HVL": sim_HVL * el.density,
          "exp_Mu": exp_Mu,
          "alpha": alpha,
          "density": el.density,
          "sim_data": sim_data
        }
      except:
        print("error on:", element_name, beam_energy)
        logging.error(traceback.format_exc())
  
if False:
  alpha_dict = {}
  sim_Mu_dict = {}
  exp_Mu_dict = {}
  for element in OUT:
    alpha_dict[element] = {}
    sim_Mu_dict[element] = {}
    exp_Mu_dict[element] = {}
    for beam in OUT[element]:
      alpha_dict[element][beam] = OUT[element][beam]["alpha"]
      sim_Mu_dict[element][beam] = OUT[element][beam]["sim_Mu"]
      exp_Mu_dict[element][beam] = OUT[element][beam]["exp_Mu"]
  alpha_df = pd.DataFrame(alpha_dict)

  print("deneysel azaltma katsayıları (cm^2/g)")
  display(pd.DataFrame(exp_Mu_dict).transpose())

  print("simülasyondan bulunan azaltma katsayıları (cm^2/g)")
  display(pd.DataFrame(sim_Mu_dict).transpose())

  print("hesaplanan tüm kesirsel alfa değerleri")
  display(alpha_df.transpose())

  energy_alpha_plot = alpha_df.plot(figsize=(20, 12), marker="o", xlabel="Beam Energy (keV)", ylabel="Alpha")
  a = labelLines(energy_alpha_plot.get_lines())
  print("alpha vs gamma energy")
  display(energy_alpha_plot.figure)
  plt.close()

  mass_alpha_plot = alpha_df.transpose().plot(figsize=(20, 12), marker="o", xlabel="Element Mass", ylabel="Alpha")
  a = labelLines(mass_alpha_plot.get_lines())
  print("alpha vs element mass")
  display(mass_alpha_plot.figure)
  plt.close()

  # hide input
  display(HTML("<script>document.querySelector('.jp-Cell-inputWrapper').remove()</script>"))


# x = np.arange(0.01, 1, 0.01)
# y = np.exp(-x)
# plt.plot(x,y)
# aValues = np.arange(0.1, 1, 0.1)
# for a in aValues:
#   y = mittag_leffler_basic(-(x)**a, a)
#   plt.plot(x,y)

# result = OUT["beryllium (9.012182)"]["88.09"]
# MuX = result["sim_HVL"] * result["exp_Mu"]
# alpha = result["alpha"]
# mittag_leffler(-1 * MuX ** alpha, alpha)

# result = OUT["beryllium (9.012182)"]["88.09"]
# MuX = result["sim_HVL"] * result["sim_Mu"]
# alpha = 1
# mittag_leffler(-1 * MuX ** alpha, alpha)

# result = OUT["thorium (232.0381)"]["208.36"]
# sim_data = result["sim_data"]
# alphas = []
# for thickness in sim_data.index:
#   MuX = thickness * result["exp_Mu"] * result["density"]
#   alpha = solve_ml_for_alpha(sim_data[thickness]/10000, MuX)
#   alphas.append(alpha)

# for element_name in element_names:
#   EL=element_properties[element_name]
#   OUT[EL.symbol] = {}
#   for beam_energy in beam_energies:
#     try:
#       OUT={"exp_Mu": EXPERIMENTAL_DATA[beam_energy]["aluminum"]}
#       OUT[EL.symbol][beam_energy] = OUT
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

