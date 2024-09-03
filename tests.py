import numpy as np
from scipy.special import gamma, factorial
import matplotlib.pyplot as plt
# from mpmath import hyper

#Locale settings
import locale
# Set to German locale to get comma decimal separater
locale.setlocale(locale.LC_NUMERIC, "de_DE")
# Tell matplotlib to use the locale we set above
plt.rcParams['axes.formatter.use_locale'] = True
plt.rcParams['text.usetex'] = True
plt.rcParams['font.size'] = 32

def solve_ml_for_alpha(Mux, result=0.5, k=0.1, precision=0.0001, max_iteration = 100000, max_sum = 100):
  i = 0
  j = 0
  prev = 0
  start_from = 0
  while True:
    j += 1
    if j > max_iteration:
      raise Exception("Exceeded max_iteration: " + str(max_iteration))
    alpha = start_from + (i * k if i * k > 0 else 0.00000000001)
    val = float(mittag_leffler_basic(-(Mux**alpha), alpha, max_sum))
    if np.abs((result - val) / result) < precision:
      return alpha
    diff = val - result
    if prev * diff < 0:
      start_from = alpha - k
      k *= 0.1
      i = 0
      prev = 0
    else:
      prev = diff
      i += 1

def mittag_leffler_basic(z, a, max_sum = 100):
  k = np.arange(max_sum).reshape(-1, 1)
  E = z**k / gamma(a*k + 1)
  return np.sum(E, axis=0)

def rising_factorial(a, n):
  arr = np.arange(0, n) + a
  return np.prod(arr)

def hyper_geometric(a_p, b_q, z, n_max = 100):
  range = np.arange(1, n_max)
  sum = 1
  for n in range:
    term = 1
    i = 0
    while len(a_p) > i or len(b_q) > i:
      if len(a_p) > i:
        term *= rising_factorial(a_p[i], n)
      if len(b_q) > i:
        term /= rising_factorial(b_q[i], n)
      i += 1
    term *= z**n/factorial(n)
    sum += term
  return sum

# n = 2
# alpha = 0.5
# arr = np.arange(0, n)
# a_n_num = arr + n
# b_n_num = a_n_num + 1 - .5
# a_n = a_n_num / n
# b_n = b_n_num / n
# print(hyper_geometric(a_n, b_n, 4))
# print(hyper(a_n, b_n, 4))

fig, ax = (None, None)
def newPlot():
  global fig, ax
  fig, ax = plt.subplots(figsize=(20, 12), tight_layout=True)
  ax.set_xlabel("$x$")
  ax.set_ylabel("$y$")
def plot(x, y, label):
  [line] = ax.plot(x, y, color="black")
  color = line.get_color()
  ax.annotate(
    label,
    xy = (x[-1], y[-1]),
    xytext = (1.07*x[-1], y[-1]),
    color = color
  )

# x^2
def plot_fractional_x_squared():
  newPlot()
  x = np.arange(0.01, 4, 0.01)
  y = x**2
  y1 = 2*x
  plot(x, y, "$y=f(x)$")
  plot(x, y1, "$y=df(x)/dx$")
  alpha_values = np.arange(0.1, 1, 0.1)
  for alpha in alpha_values:
    y_alpha = (2 * (x ** (2 - alpha))) / gamma(3 - alpha)
    plot(x, y_alpha, "$\\alpha=" + "{:.1f}".format(alpha).replace(".", ",") + "$")

# exp[-mu*x]
def plot_fractional_exp_decrease(mu = 1):
  newPlot()
  x = np.arange(0, 4, 0.01)
  y = np.exp(-mu*x)
  y1 = -mu * np.exp(-mu*x)
  plot(x, y, "y")
  plot(x, y1, "dy/dx")
  alpha_values = np.arange(0.1, 1, 0.1)
  for alpha in alpha_values:
    y_alpha = mittag_leffler_basic(-(x*mu)**alpha, alpha)
    plot(x, y_alpha, str(alpha))

# v2 exp[-(mu*x)^n]
def fractional_exp_decrease_2(x, alpha, n = 1, mu = 1):
  part_1 = -mu**n * x**(n - alpha)
  part_2 = gamma(n + 1) / gamma(n + 1 - alpha)
  part_3 = np.empty(len(x), dtype=np.float64)
  # for index, x_value in enumerate(x):
  #   part_3[index] = hyper(create_series(n), create_series(n, alpha), -(mu*x_value)**n)
  part_3 = hyper_geometric(create_series(n), create_series(n, alpha), -(mu*x)**n)
  return part_1 * part_2 * part_3

def create_series(n, alpha = 1):
  a = np.empty(n, dtype=np.float64)
  i = 1
  while i <= n:
    a[i - 1] = (n + i - alpha) / n
    i+=1
  return a

# düzeltme fonksiyonu:
def g(alpha):
  return alpha

def plot_fractional_exp_decrease_2(order = 1, mu = 1):
  newPlot()
  x = np.arange(0, 4, 0.01)
  y = np.exp(-(mu*x)**order)
  y1 = -mu * order * x**(order-1) * np.exp(-(mu*x)**order)
  plot(x, y1, "dy/dx")
  # plot(x, y, "y")
  plot(x, y-1, "y-1")
  alpha_values = np.arange(0.1, 1, 0.1)
  for alpha in alpha_values:
    y_alpha = fractional_exp_decrease_2(x, alpha, order, mu)
    plot(x, y_alpha, str(alpha))
  # plot(x, fractional_exp_decrease_2(x, 0.96, order, mu), str(0.96))

plot_fractional_x_squared()
# plot_fractional_exp_decrease()
# plot_fractional_exp_decrease_2()

def test1():
  x = np.arange(0, 4, 0.1)
  y = np.exp(-x**2)
  y1 = -2 * x * np.exp(-x**2)
  ya = y-1
  newPlot()
  plot(x, y1, "dy/dx")
  plot(x, ya, "y1a")
