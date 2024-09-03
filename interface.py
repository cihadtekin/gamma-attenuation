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
#from labellines import labelLine, labelLines
import os
#from IPython.display import display, HTML
from scipy.special import gamma

#Locale settings
import locale
# Set to German locale to get comma decimal separater
locale.setlocale(locale.LC_NUMERIC, "de_DE")
# Tell matplotlib to use the locale we set above
plt.rcParams['axes.formatter.use_locale'] = True

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
    #ind=el.name + " (" + str(el.mass) + ")"
    ind=el.name
    OUT[ind] = {}

    for beam_energy in beam_energies:
      sim_file = COUNTS_DIR + el.name + "/" + beam_energy + ".csv"
      if not Path(sim_file).exists():
        continue

      try:
        exp_Mu = EXPERIMENTAL_DATA[beam_energy][el.name]
        exp_HVL = -LNOFANHALF/exp_Mu
        sim_data = pd.read_csv(sim_file, sep=";", index_col=0)["count"]
        sim_linear_data = -np.log(sim_data[sim_data > 0]/BEAM_COUNT)
        [sim_Mu] = curve_fit(linear, sim_linear_data.index.values, sim_linear_data.values)[0]
        sim_Mu = sim_Mu / el.density
        sim_HVL = -LNOFANHALF/sim_Mu

        # calculate alpha
        # TODO: Mu ve HVL için tam tersini yap ve alfa değerlerini karşılaştır (değişiyor mu).
        Mux = exp_HVL * sim_Mu
        alpha = solve_ml_for_alpha(0.5, Mux)

        OUT[ind][beam_energy] = {
          "sim_Mu": sim_Mu,
          "sim_HVL": sim_HVL,
          "exp_Mu": exp_Mu,
          "exp_HVL": exp_HVL,
          "alpha": alpha,
          "density": el.density,
          "sim_data": sim_data,
          "sim_linear_data": sim_linear_data
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


if True:
  ALPHAS_BY_ELEMENT_DIR = "alphas-by-element"
  ALPHAS_BY_GAMMA_DIR = "alphas-by-gama"
  Path(ALPHAS_BY_ELEMENT_DIR).mkdir(parents=True, exist_ok=True)
  Path(ALPHAS_BY_GAMMA_DIR).mkdir(parents=True, exist_ok=True)

  plt.rcParams['text.usetex'] = True
  plt.rcParams['font.size'] = 32
  plt.rcParams['mathtext.fontset'] = 'stix'
  plt.rcParams['font.family'] = 'STIXGeneral'

  fig, ax = (None, None)
  def newPlot(ylabel = "$y$", xlabel = "$x$"):
    global fig, ax
    fig, ax = plt.subplots(figsize=(20, 12), tight_layout=True)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
  def plot(x, y, path, label = None):
    [line] = ax.plot(x, y, color="black", marker="o")
    color = line.get_color()
    if label:
      ax.annotate(
        label,
        xy = (x[-1], y[-1]),
        xytext = (1.02*x[-1], y[-1]),
        color = color
      )
    plt.savefig(path)

  # experimental Mu, alpha, HVL tables
  if True:
    exp_mu_table = []
    exp_HVL_table = []
    exp_mu_table.append([""] + list(map(lambda en: en.replace(".", ","), beam_energies)))
    exp_HVL_table.append([""] + list(map(lambda en: en.replace(".", ","), beam_energies)))
    sim_mu_table = []
    sim_HVL_table = []
    sim_mu_table.append([""] + list(map(lambda en: en.replace(".", ","), beam_energies)))
    sim_HVL_table.append([""] + list(map(lambda en: en.replace(".", ","), beam_energies)))
    alpha_table = []
    alpha_table.append([""] + list(map(lambda en: en.replace(".", ","), beam_energies)))

    for element in element_names:
      el = element_properties[element]

      exp_mu_table_row = ["$" + "_{" + str(el.number) + "}" + el.symbol + "$"]
      exp_HVL_table_row = ["$" + "_{" + str(el.number) + "}" + el.symbol + "$"]
      exp_mu_table.append(exp_mu_table_row)
      exp_HVL_table.append(exp_HVL_table_row)
      sim_mu_table_row = ["$" + "_{" + str(el.number) + "}" + el.symbol + "$"]
      sim_HVL_table_row = ["$" + "_{" + str(el.number) + "}" + el.symbol + "$"]
      sim_mu_table.append(sim_mu_table_row)
      sim_HVL_table.append(sim_HVL_table_row)
      alpha_table_row = ["$" + "_{" + str(el.number) + "}" + el.symbol + "$"]
      alpha_table.append(alpha_table_row)

      for beam in beam_energies:
        exp_mu_table_row.append("{:.4f}".format(OUT[element][beam]["exp_Mu"]).replace(".", ","))
        exp_HVL_table_row.append("{:.3f}".format(OUT[element][beam]["exp_HVL"]).replace(".", ","))
        sim_mu_table_row.append("{:.4f}".format(OUT[element][beam]["sim_Mu"]).replace(".", ","))
        sim_HVL_table_row.append("{:.3f}".format(OUT[element][beam]["sim_HVL"]).replace(".", ","))
        alpha_table_row.append("{:.4f}".format(OUT[element][beam]["alpha"]).replace(".", ","))

    # print("\\\\\n".join(list(map(lambda row: "&".join(row), exp_mu_table))))
    # print("\\\\\n".join(list(map(lambda row: "&".join(row), exp_HVL_table))))
    # print("\\\\\n".join(list(map(lambda row: "&".join(row), sim_mu_table))))
    # print("\\\\\n".join(list(map(lambda row: "&".join(row), sim_HVL_table))))
    print("\\\\\n".join(list(map(lambda row: "&".join(row), alpha_table))))
  
  alphas_by_gamma = {}
  for element in element_names:
    el = element_properties[element]
    alphas_by_element = []

    for beam in beam_energies:
      item = OUT[element][beam]
      alphas_by_element.append(item["alpha"])
      if beam not in alphas_by_gamma:
        alphas_by_gamma[beam] = []
      alphas_by_gamma[beam].append(item["alpha"])

      # all props table
      if False:
        print(""
          + "$" + "_{" + str(el.number) + "}" + el.symbol + "$&"
          + "{:.2f}".format(float(item["beam"])) + "&"
          + "{:.5f}".format(item["sim_Mu"]) + "&"
          + "{:.5f}".format(item["exp_Mu"]) + "&"
          + "{:.5f}".format(item["exp_HVL"]) + "&"
          + "{:.5f}".format(item["alpha"])
          + "\\\\"
        )

      # linear mu graphs
      if False:
        newPlot("$ln\\left(\\frac{I(x)}{I_0}\\right)$", "$x$")
        sim_linear_data = item["sim_linear_data"]
        plot(
          sim_linear_data.index.values,
          sim_linear_data.values,
          COUNTS_DIR + "/" + element + "/mu-" + beam + ".png"
        )

    # alpha graphs by element
    if False:
      el = element_properties[element]
      if False:
        print(f'''\\begin{{figure}}[H]
  \\centering
  \\includegraphics[scale=0.2]{{{ALPHAS_BY_ELEMENT_DIR}/{element}.png}}
  \\caption{{$_{{{el.number}}} {el.symbol}$ için $\\alpha$'nın gama enerjisine göre değişimi}}
  \\label{{fig:alpha-by-element-{element}}}
\\end{{figure}}'''
        )
      if False:
        newPlot("$\\alpha$", "Gama enerjisi $(keV)$")
        plot(
          list(map(lambda e: float(e), beam_energies)),
          alphas_by_element,
          ALPHAS_BY_ELEMENT_DIR + "/" + element + ".png"
        )

  # alpha graphs by gamma
  if False:
    for beam in beam_energies:
      if False:
        print(f'''\\begin{{figure}}[H]
  \\centering
  \\includegraphics[scale=0.2]{{{ALPHAS_BY_GAMMA_DIR}/{beam}.png}}
  \\caption{{{beam.replace(".", ",")} keV enerjili gama ışınları için $\\alpha$'nın materyale göre değişimi}}
  \\label{{fig:alpha-by-gamma-{beam}}}
\\end{{figure}}'''
        )
      if False:
        plt.rcParams['font.size'] = 22
        newPlot("$\\alpha$", "Materyal")
        plot(
          list(map(lambda e: "$" + "_{" + str(element_properties[e].number) + "}" + element_properties[e].symbol + "$", element_names)),
          alphas_by_gamma[beam],
          ALPHAS_BY_GAMMA_DIR + "/" + beam + ".png"
        )


# result = OUT["beryllium (9.012182)"]["88.09"]
# MuX = result["sim_Mu"] * result["exp_HVL"]
# alpha = result["alpha"]
# mittag_leffler_basic(-1 * (MuX ** alpha), alpha)

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

