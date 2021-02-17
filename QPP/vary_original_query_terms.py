import numpy as np
import matplotlib.pyplot as plt
from numpy.distutils.system_info import x11_info

nqc_jm_rlm = np.array([0.685, 0.6861])
nqc_jm_w2v = np.array([0.6904, 0.6893])
nqc_wrig_rlm = np.array([0.7121, 0.713])
nqc_wrig_w2v = np.array([0.7968, 0.7963])

cw_jm_rlm = np.array([0.4593, 0.4595, 0.4578, 0.4589])
cw_jm_w2v = np.array([0.4736, 0.4724, 0.4732, 0.4729])
cw_wrig_rlm = np.array([0.5375, 0.5379, 0.5362, 0.5368])
cw_wrig_w2v = np.array([0.5441, 0.5449, 0.5443, 0.5437])

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

x = np.array([1, 2, 3, 4])
read_data = [nqc_jm_rlm, nqc_jm_w2v, nqc_wrig_rlm, nqc_wrig_w2v]
fig, axes = plt.subplots(nrows=1, ncols=2)
xticks = np.around(np.linspace(1, 4, 4, endpoint=True), 2)
yticks = np.around(np.linspace(0.44, 0.55, 12, endpoint=True), 2)

axes[0].plot(x, cw_jm_rlm, label='NQC$_{LR}$(JM$_{RLM}$)', linewidth=3, color='maroon')
axes[0].plot(x, cw_wrig_rlm, label='NQC$_{LR}$(WRIG$_{RLM}$)', linewidth=3, color='green')

axes[0].scatter(x, cw_jm_rlm, marker='D', s=100, color='maroon')
axes[0].scatter(x, cw_wrig_rlm, marker='P', s=100, color='green')

# axes[1].plot(x, nqc_jm_w2v, label='NQC$_{LR}$(JM$_{W2V}$)', linewidth=3, color='maroon')
# axes[1].plot(x, nqc_wrig_w2v, label='NQC$_{LR}$(WRIG$_{W2V}$)', linewidth=3, color='green')
#
# axes[1].scatter(x, nqc_jm_w2v, marker='X', s=100, color='maroon')
# axes[1].scatter(x, nqc_wrig_w2v, marker='8', s=100, color='green')

axes[0].set_xticks(xticks)
axes[0].set_yticks(yticks)
# axes[1].set_xticks(xticks)
# axes[1].set_yticks(yticks)

axes[0].set_xlabel('$|Q|-m$', fontsize=20)
axes[0].set_ylabel("Spearman's $\\rho$", fontsize=20)
# axes[0].set_ylabel('$P(S|Q,\epsilon_Q)$', fontsize=25, fontweight='bold')

# axes[1].set_xlabel('$|Q|-m$', fontsize=20)
# axes[1].set_ylabel("Spearman's $\\rho$", fontsize=20)
# axes[1].set_ylabel('$P(S|Q,\epsilon_Q)$', fontsize=25, fontweight='bold')


axes[0].legend(loc="best", fontsize=15)
# axes[1].legend(loc="best", fontsize=15)

plt.subplots_adjust(left=0.10, right=0.70, bottom=0.50, top=0.87)

plt.show()
