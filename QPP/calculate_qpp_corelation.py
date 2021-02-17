import sys, numpy as np
from operator import itemgetter
from scipy import stats
import pandas as pd
import matplotlib.pyplot as plt

if len(sys.argv) < 3:
    print('Needs 2 arguments - <qid \t AP> <qid \t NQC>')
    exit(0)

arg_map = sys.argv[1]
arg_nqc = sys.argv[2]


def read_file(file):
    fp = open(file)
    scores = []
    for line in fp.readlines():
        scores.append(float(line.split('\t')[1]))
    return scores


lm_map = read_file(arg_map)
# print('map : ', lm_map)
lm_nqc = read_file(arg_nqc)
# print('nqc : ', lm_nqc)

# pearson co-relation test
# list1 = list(lm_nqc_dict)
# print(list1)
# nqc_score_lm = itemgetter(*list(lm_nqc_dict))(lm_nqc_dict)
# print(nqc_score_lm)
# nqc_score_drmm = itemgetter(*list(drmm_nqc_dict))(drmm_nqc_dict)
# print(nqc_score_drmm)
# corr, _ = pearsonr(lm_map, lm_nqc)
# print('Pearsons correlation: %.3f', corr)

# spearman's rank co-relation
# Calculate the rank of x's
xranks = pd.Series(lm_map).rank()
# print("Rankings of X:", xranks)
#
# # Caclulate the ranking of the y's
yranks = pd.Series(lm_nqc).rank()
# print("Rankings of Y:", yranks)

# Calculate Pearson's correlation coefficient on the ranked versions of the data
# print("Spearman's Rank correlation:", scipy.stats.pearsonr(xranks, yranks)[0])
corrs, _ = stats.spearmanr(lm_map, lm_nqc)
print("Spearman's Rank correlation: %.5f" % corrs)

# Calculating Kendall Rank correlation
corr, _ = stats.kendalltau(lm_map, lm_nqc)
print('Kendall Rank correlation: %.5f' % corr)

# Calculate gini coefficient
# lm_nqc_sorted = sorted(lm_nqc)
# print(lm_nqc_sorted)
# mean = 0
# inner_sum = 0
# outer_sum = 0
#
# for value in lm_nqc_sorted:
#     mean = sum(lm_nqc_sorted) / len(lm_nqc_sorted)
# print(mean)
#
# for i in lm_nqc_sorted:
#     for j in lm_nqc_sorted:
#         inner_sum += abs(i - j)
#     outer_sum += inner_sum
# print(outer_sum)
# gini = outer_sum / (2 * pow(len(lm_nqc_sorted), 2) * mean)
# print("gini coefficient : %0.4f" % gini)

# lm_rho = np.array([0.4048, 0.4547, 0.4692, 0.4705, 0.4857, 0.4985, 0.5044, 0.5065, 0.5255, 0.5486])
# lm_tau = np.array([0.2767, 0.3241, 0.3371, 0.3388, 0.3388, 0.3437, 0.3518, 0.3535, 0.3714, 0.3845])
#
#
# def gini(arr):
#     ## first sort
#     lm_rho_sorted = arr.copy()
#     lm_rho_sorted.sort()
#     n = lm_rho_sorted.size
#     coef_ = 2. / n
#     const_ = (n + 1.) / n
#     weighted_sum = sum([(i+1)*yi for i, yi in enumerate(lm_rho_sorted)])
#     return coef_*weighted_sum/(lm_rho_sorted.sum()) - const_
#
#
# # gini = gini(lm_rho)
# # print("gini : ", gini)
# # X_lorenz = lm_rho.cumsum() / lm_rho.sum()
#
# gini = gini(lm_tau)
# print("gini : ", gini)
# X_lorenz = lm_tau.cumsum() / lm_tau.sum()
#
# X_lorenz = np.insert(X_lorenz, 0, 0)
# print(X_lorenz[0], X_lorenz[-1])
#
# fig, ax = plt.subplots(figsize=[6, 6])
# ## scatter plot of Lorenz curve
# ax.scatter(np.arange(X_lorenz.size)/(X_lorenz.size-1), X_lorenz, marker='x', color='darkgreen', s=100)
# ## line plot of equality
# ax.plot([0, 1], [0, 1], color='k')
# plt.show()