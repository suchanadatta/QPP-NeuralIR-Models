# contour plot

# from matplotlib import pyplot as plt
# import numpy as np
# import random
#
# bins, k = np.mgrid[10:50:5j, 10:100:10j]
# print(bins, '\n\n', k)
#
# rho = [random.random() for j in range(0, 50)]
# rho = np.array([*rho])
# rho = np.reshape(rho, [5, 10])
# print(rho)
# fig, axes = plt.subplots(nrows=1, ncols=1)
# levels = np.linspace(np.min(rho), np.max(rho), 20)
# ticks = np.linspace(np.min(rho), np.max(rho), 10)
# c = axes.contourf(k, bins, rho, levels=levels, extend='both')
# c1 = axes.contour(k, bins, rho, levels=ticks, extend='both', colors='k', linewidths=0.25)
# axes.clabel(c1, ticks, inline=True, fontsize=10)
# plt.colorbar(c, ticks=ticks)
# plt.show()


import numpy as np
import matplotlib.pyplot as plt
import os, sys

from numpy.distutils.system_info import x11_info

data_plot = np.genfromtxt('plot', dtype=np.float64, delimiter='\t', skip_header=0)

print(data_plot)

SMALL_SIZE = 10
MEDIUM_SIZE = 12
BIGGER_SIZE = 28

plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
plt.rc('axes', titlesize=SMALL_SIZE)     # fontsize of the axes title
plt.rc('axes', labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=MEDIUM_SIZE)    # fontsize of the tick labels
plt.rc('ytick', labelsize=MEDIUM_SIZE)    # fontsize of the tick labels
plt.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize
plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title

fig, axes = plt.subplots(nrows=1, ncols=2)
xticks = np.linspace(0, np.max(data_plot[:, 0]), 11, endpoint=True)
yticks_1 = np.linspace(0, 1, 11, endpoint=True)
yticks_2 = np.linspace(0, 1, 11, endpoint=True)

[axes[0].plot(data_plot[:, 0], data_plot[:, j[0]], label=j[1]) for j in [(1, 'LM'), (3, 'DRMM')]]
[axes[1].plot(data_plot[:, 0], data_plot[:, j[0]], label=j[1]) for j in [(2, 'LM'), (4, 'DRMM')]]

axes[0].set_xticks(xticks)
axes[0].set_yticks(yticks_1)
axes[1].set_xticks(xticks)
axes[1].set_yticks(yticks_2)

axes[0].set_xlabel("Top docs", fontsize=18, fontweight='bold')
axes[0].set_ylabel("Spearman's Rho", fontsize=18, fontweight='bold')
axes[0].set_title("LM vs. DRMM", fontsize=18, fontweight='bold')
axes[0].legend(loc='best')

axes[1].set_xlabel("Top docs", fontsize=18, fontweight='bold')
axes[1].set_ylabel("Kendall's Tau", fontsize=18, fontweight='bold')
axes[1].set_title("LM vs. DRMM", fontsize=18, fontweight='bold')
axes[1].legend(loc='best')

plt.show()