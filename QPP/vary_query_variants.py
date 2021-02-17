import numpy as np
import matplotlib.pyplot as plt
from numpy.distutils.system_info import x11_info

nqc_jm_rlm = np.array([0.6264, 0.685, 0.5686, 0.581, 0.4812])
nqc_jm_w2v = np.array([0.6349, 0.6904, 0.6149, 0.5839, 0.5442])
nqc_wrig_rlm = np.array([0.6669, 0.7121, 0.6761, 0.6447, 0.6364])
nqc_wrig_w2v = np.array([0.7445, 0.7968, 0.6986, 0.7119, 0.6801])
nqc_lr = np.array([0.6292, 0.6292, 0.6292, 0.6292, 0.6292])

cw_jm_rlm = np.array([0.3824, 0.4593, 0.3671, 0.3789, 0.3329])
cw_jm_w2v = np.array([0.4213, 0.4736, 0.3826, 0.3519, 0.3103])
cw_wrig_rlm = np.array([0.4889, 0.5375, 0.4721, 0.437, 0.4016])
cw_wrig_w2v = np.array([0.4915, 0.5441, 0.4327, 0.451, 0.4112])
cw_lr = np.array([0.3921, 0.3921, 0.3921, 0.3921, 0.3921])

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

x = np.array([5, 10, 15, 20, 25])
read_data = [nqc_jm_rlm, nqc_jm_w2v, nqc_wrig_rlm, nqc_wrig_w2v, nqc_lr]
fig, axes = plt.subplots(nrows=1, ncols=2)
xticks = np.linspace(5, 25, 5, endpoint=True)
yticks = np.linspace(0.5, 0.9, 5, endpoint=True)

axes[0].plot(x, nqc_jm_rlm, label='NQC$_{LR}$(JM$_{RLM}$)', linewidth=3)
axes[0].plot(x, nqc_wrig_rlm, label='NQC$_{LR}$(WRIG$_{RLM}$)', linewidth=3)
axes[0].plot(x, nqc_lr, label='NQC$_{LR}$(None)', linewidth=3)

axes[0].scatter(x, nqc_jm_rlm, marker='D', s=100)
axes[0].scatter(x, nqc_wrig_rlm, marker='P', s=100)
axes[0].scatter(x, nqc_lr, marker='^', s=100)

# axes[1].plot(x, nqc_jm_w2v, label='NQC$_{LR}$(JM$_{W2V}$)', linewidth=3)
# axes[1].plot(x, nqc_wrig_w2v, label='NQC$_{LR}$(WRIG$_{W2V}$)', linewidth=3)
# axes[1].plot(x, nqc_lr, label='NQC$_{LR}$(None)', linewidth=3)
#
# axes[1].scatter(x, nqc_jm_w2v, marker='X', s=100)
# axes[1].scatter(x, nqc_wrig_w2v, marker='8', s=100)
# axes[1].scatter(x, nqc_lr, marker='s', s=100)

axes[0].set_xticks(xticks)
axes[0].set_yticks(yticks)
# axes[1].set_xticks(xticks)
# axes[1].set_yticks(yticks)

axes[0].set_xlabel('$|\epsilon_Q|$', fontsize=25)
axes[0].set_ylabel("Spearman's $\\rho$", fontsize=20)
# axes[0].set_ylabel('$P(S|Q,\epsilon_Q)$', fontsize=25, fontweight='bold')

# axes[1].set_xlabel('$|\epsilon_Q|$', fontsize=25)
# axes[1].set_ylabel("Spearman's $\\rho$", fontsize=20)
# axes[1].set_ylabel('$P(S|Q,\epsilon_Q)$', fontsize=25, fontweight='bold')


axes[0].legend(loc="best", fontsize=15)
# axes[1].legend(loc="best", fontsize=15)

plt.subplots_adjust(left=0.10, right=0.70, bottom=0.50, top=0.87)

plt.show()

# =================================================
# yticks = np.linspace(0.25, 0.65, 5, endpoint=True)
#
# axes[0].plot(x, cw_jm_rlm, label='NQC$_{LR}$(JM$_{RLM}$)', linewidth=3)
# axes[0].plot(x, cw_wrig_rlm, label='NQC$_{LR}$(WRIG$_{RLM}$)', linewidth=3)
# axes[0].plot(x, cw_lr, label='NQC$_{LR}$(None)', linewidth=3)
#
# axes[0].scatter(x, cw_jm_rlm, marker='D', s=100)
# axes[0].scatter(x, cw_wrig_rlm, marker='P', s=100)
# axes[0].scatter(x, cw_lr, marker='^', s=100)
#
# # axes[1].plot(x, cw_jm_w2v, label='NQC$_{LR}$(JM$_{W2V}$)', linewidth=3)
# # axes[1].plot(x, cw_wrig_w2v, label='NQC$_{LR}$(WRIG$_{W2V}$)', linewidth=3)
# # axes[1].plot(x, cw_lr, label='NQC$_{LR}$(None)', linewidth=3)
# #
# # axes[1].scatter(x, cw_jm_w2v, marker='X', s=100)
# # axes[1].scatter(x, cw_wrig_w2v, marker='8', s=100)
# # axes[1].scatter(x, cw_lr, marker='s', s=100)
#
# axes[0].set_xticks(xticks)
# axes[0].set_yticks(yticks)
# # axes[1].set_xticks(xticks)
# # axes[1].set_yticks(yticks)
#
# axes[0].set_xlabel('$|\epsilon_Q|$', fontsize=25)
# axes[0].set_ylabel("Spearman's $\\rho$", fontsize=20)
# # axes[0].set_ylabel('$P(S|Q,\epsilon_Q)$', fontsize=25, fontweight='bold')
#
# # axes[1].set_xlabel('$|\epsilon_Q|$', fontsize=25)
# # axes[1].set_ylabel("Spearman's $\\rho$", fontsize=20)
# # axes[1].set_ylabel('$P(S|Q,\epsilon_Q)$', fontsize=25, fontweight='bold')
#
#
# axes[0].legend(loc="best", fontsize=15)
# # axes[1].legend(loc="best", fontsize=15)
#
# plt.subplots_adjust(left=0.10, right=0.70, bottom=0.50, top=0.87)
#
# plt.show()
#
#
#
