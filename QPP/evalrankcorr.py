# from scipy import stats
# import sys
#
#
# def rankCorr(x, y):
#     rho, pval = stats.spearmanr(x, y)
#     tau, pval = stats.kendalltau(x, y)
#     print('S-rho = {:.4f}, K-tau = {:.4f}'.format(rho, tau))
#
#
# if len(sys.argv) < 1:
#     print('usage: python rankcorr.py <values file>')
#     sys.exit(0)
#
# values_file = open(sys.argv[1], "r")
# lines = values_file.readlines()
#
# col1 = []
# col3 = []
# col2 = []
# col4 = []
# for line in lines:
#     tokens = line.split('\t')
#     col1.append(tokens[0])
#     col3.append(tokens[2])
#     # col2.append(tokens[1])
#     # col4.append(tokens[3])
#
# values_file.close()
#
# rankCorr(col1, col3)


from scipy import stats
import sys, math


def reportRankCorr(x, y):
    rho, pval = stats.spearmanr(x, y)
    tau, pval = stats.kendalltau(x, y)
    print('S-rho = {:.4f}, K-tau = {:.4f}'.format(rho, tau))

    #also compute the avg shift in ranks
    i = 1
    rmse = 0
    for x_i in x:
        j = y.index(x_i)
        rmse += abs(i-j)
        i+= 1
    print('rmse = {:.4f}'.format(rmse/len(x)))


if len(sys.argv) < 1:
    print ('usage: python evalrankcorr.py <values file>')
    sys.exit(0)
values_file = open(sys.argv[1], "r")
lines = values_file.readlines()
x = []
y = []
for line in lines:
    tokens = line.split()
    x.append(tokens[0])
    y.append(tokens[1])
values_file.close()
reportRankCorr(x, y)