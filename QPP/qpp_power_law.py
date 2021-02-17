import sys
import numpy as np
import math
import pandas as pd
from scipy import stats

if len(sys.argv) < 5:
    print('Needs 4 arguments - \n1. TREC initial query based LM .res / reranked file (reranked by DRMM)\n'
          '2. TREC initial query .AP file\n'
          '3. res file path\n'
          '4. No. of top documents to be considered')
    exit(0)

arg_res_file = sys.argv[1]
arg_ap_file = sys.argv[2]
arg_res_file_path = sys.argv[3]
arg_top_docs = int(sys.argv[4])

trec_power_Q = {}


def compute_power_law_trec(score_list, qid):
    alpha_hat = 0
    score_list = np.array(score_list).astype(np.float)
    # print('score list : ', score_list)
    # print('min of the score list : ', min(score_list))
    for score in score_list:
        alpha_hat += math.log(abs(score / min(score_list)))
        # print("alpha_hat :", alpha_hat)
    alpha_hat = 1 + len(score_list) * pow(alpha_hat, -1)
    # print("final alpha : ", alpha_hat)
    trec_power_Q[qid] = round(alpha_hat, 4)
    # print("TREC res file power dict : ", trec_power_Q)


def power_law_trec_query(trec_res_file, topdocs):
    qid = ""
    count = 0
    per_query_score_list = []
    fp = open(trec_res_file)
    for line in fp.readlines():
        parts = line.split('\t')
        if qid == "" or parts[0] == qid:
            if count < topdocs:
                qid = parts[0]
                score = parts[3]
                per_query_score_list.append(score)
                count = count + 1
        elif parts[0] != qid:
            # print('query : ', qid, '\t', per_query_score_list)
            compute_power_law_trec(per_query_score_list, qid)
            per_query_score_list = []
            count = 0
            qid = parts[0]
            score = parts[3]
            per_query_score_list.append(score)
            count = count + 1
    # print('query : ', qid, '\t', per_query_score_list)
    compute_power_law_trec(per_query_score_list, qid)


power_law_trec_query(arg_res_file, arg_top_docs)
print("TREC res file power dict : ", trec_power_Q)

fp = open(arg_ap_file)
ap_scores = []
nqc_power_scores = []
for line in fp.readlines():
    ap_scores.append(float(line.split('\t')[1]))
for key in trec_power_Q:
    nqc_power_scores.append(trec_power_Q[key])

xranks = pd.Series(ap_scores).rank()
# print("Rankings of X:", xranks)
yranks = pd.Series(nqc_power_scores).rank()
# print("Rankings of Y:", yranks)
rho, _ = stats.spearmanr(ap_scores, nqc_power_scores)
print("\nSpearman's Rank correlation:", round(rho, 4))

tau, _ = stats.kendalltau(ap_scores, nqc_power_scores)
print('Kendall Rank correlation: %.5f' % tau)