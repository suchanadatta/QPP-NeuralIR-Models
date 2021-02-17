import sys
from math import sqrt
import numpy as np
import pandas as pd
from scipy import stats

if len(sys.argv) < 8:
    print('Needs 7 arguments - \n1. TREC initial query based LM reranked file (reranked by DRMM)\n'
          '2. UQV-TREC query variants based LM reranked file (reranked by DRMM)\n'
          '3. TREC initial query .AP file\n'
          '4. res file path\n'
          '5. No. of top documents retrieved by initial query in the initial.res file\n'
          '6. No. of top documents retrieved by query variant in the variant.res file\n'
          '7. No. of top scores to be considered for each variant')
    exit(0)

arg_trec_prerank_file = sys.argv[1]
arg_uqv_prerank_file = sys.argv[2]
arg_trec_ap_file = sys.argv[3]
arg_res_path = sys.argv[4]
arg_top_docs_iq = int(sys.argv[5])
arg_top_docs_vq = int(sys.argv[6])
arg_top_scores_vq = int(sys.argv[7])

# fw_variance = open(arg_res_path + 'TD-' + str(arg_top_docs_iq) + 'TS-' + str(arg_top_docs_vq) + '_variance.res', 'w')
# fw_gini = open(arg_res_path + 'TD-' + str(arg_top_docs_iq) + 'TS-' + str(arg_top_docs_vq) + '_gini.res', 'w')

trec_v_Q = {}
trec_g_Q = {}
uqv_v_Q = {}
uqv_g_Q = {}
nqc_v_dict = {}
nqc_g_dict = {}


def compute_variance_trec(score_list, qid):
    variance = 0
    score_list = np.array(score_list).astype(np.float)
    mu = sum(score_list) / len(score_list)
    # print("mu : ", mu)
    for score in score_list:
        variance += pow((score - mu), 2)
        # print("variance : ", variance)
    variance = sqrt(1/len(score_list) * variance)
    # print("variance here : ", variance)
    trec_v_Q[qid] = round(variance, 6)
    # print("TREC res file variance dict : ", trec_v_Q)


def variance_trec_query(trec_res_file, topdocs):
    qid = ""
    count = 0
    per_query_score_list = []
    fp = open(trec_res_file)
    for line in fp.readlines():
        parts = line.split('\t')
        if qid == "" or parts[0] == qid:
            if count < topdocs:
                qid = parts[0]
                score = parts[4]
                per_query_score_list.append(score)
                count = count + 1
        elif parts[0] != qid:
            # print('query : ', qid, '\t', per_query_score_list)
            compute_variance_trec(per_query_score_list, qid)
            per_query_score_list = []
            count = 0
            qid = parts[0]
            score = parts[4]
            per_query_score_list.append(score)
            count = count + 1
    # print('query : ', qid, '\t', per_query_score_list)
    compute_variance_trec(per_query_score_list, qid)


def compute_variance_uqv(score_list, varscores):
    # print("sorted list size : ", len(score_list))
    score_list = np.array(score_list).astype(np.float)
    score_list = score_list[0:varscores]
    # print('sub-score list size : ', len(score_list))
    mu = sum(score_list) / len(score_list)
    # print("mu one uqc : ", mu)
    variance = 0
    for score in score_list:
        variance += pow((score - mu), 2)
        # print("var : ", variance)
    variance = sqrt(variance * (1 / len(score_list)))
    # print("variance one uqc : ", variance)
    return round(variance, 6)


def variance_uqv_query(uqv_res_file, topdocs, varscores):
    qid = ""
    count = 0
    fp = open(uqv_res_file)
    per_query_score_list = []
    per_query_QV_list = []
    for line in fp.readlines():
        parts = line.split('\t')
        if qid == "" or parts[0] == qid:
            if count < topdocs:
                per_query_score_list.append(parts[4])
                qid = parts[0]
                count += 1
            else:
                # print('query : ', qid, '\t', 'score list size : ', len(per_query_score_list))
                per_query_score_list = sorted(per_query_score_list, reverse=True)
                variance = compute_variance_uqv(per_query_score_list, varscores)
                per_query_QV_list.append(variance)
                count = 1
                qid = parts[0]
                per_query_score_list = [parts[4]]
        elif parts[0] != qid:
            # print('query : ', qid, '\t', 'score list size : ', len(per_query_score_list))
            per_query_score_list = sorted(per_query_score_list, reverse=True)
            variance = compute_variance_uqv(per_query_score_list, varscores)
            per_query_QV_list.append(variance)
            uqv_v_Q[qid] = per_query_QV_list
            # print('query : ', qid, '\t', 'no. of query variants : ', len(per_query_QV_list))
            count = 1
            qid = parts[0]
            per_query_score_list = [parts[4]]
            per_query_QV_list = []
    # print('query : ', qid, '\t', 'score list size : ', len(per_query_score_list))
    per_query_score_list = sorted(per_query_score_list, reverse=True)
    variance = compute_variance_uqv(per_query_score_list, varscores)
    per_query_QV_list.append(variance)
    uqv_v_Q[qid] = per_query_QV_list
    # print('query : ', qid, '\t', 'no. of query variants : ', len(per_query_QV_list))
    # print("final list : ", uqv_v_Q)


def compute_gini_trec(score_list, qid):
    i = 1
    weighted_sum = 0
    gini_array = np.array(score_list).astype(np.float)
    gini_array.sort()
    # print(gini_array)
    gini_array_size = len(gini_array)
    # print(gini_array_size)
    coef = 2 / gini_array_size
    # print(coef)
    const = (gini_array_size + 1) / gini_array_size
    # print(const)
    while i <= gini_array_size:
        for yi in gini_array:
            weighted_sum += i * yi
            i += 1
    # print(weighted_sum, "\t", i)
    gini = coef * weighted_sum / (gini_array.sum()) - const
    trec_g_Q[qid] = round(gini, 6)


def gini_trec_query(uqv_res_file, topdocs):
    qid = ""
    count = 0
    per_query_score_list = []
    fp = open(uqv_res_file)
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
            compute_gini_trec(per_query_score_list, qid)
            per_query_score_list = []
            count = 0
            qid = parts[0]
            score = parts[3]
            per_query_score_list.append(score)
            count = count + 1
    # print('query : ', qid, '\t', per_query_score_list)
    compute_gini_trec(per_query_score_list, qid)


def compute_gini_uqv(score_list, varscores):
    # print("list : ", score_list)
    score_list = np.array(score_list).astype(np.float)
    scores = score_list[0:varscores]
    # print('score list : ', score_list)
    scores.sort()
    # print('scores : ', scores)
    i = 1
    weighted_sum = 0
    coef = 2 / len(scores)
    # print('coef : ', coef)
    const = (len(scores) + 1) / len(scores)
    # print('const : ', const)
    while i < len(scores) + 1:
        for yi in scores:
            weighted_sum += i * yi
            i += 1
    # print('sum : ', weighted_sum)
    gini = ((coef * weighted_sum) / scores.sum()) - const
    # print('gini : ', gini)
    return round(gini, 6)


def gini_uqv_query(uqv_res_file, topdocs, varscores):
    qid = ""
    count = 0
    fp = open(uqv_res_file)
    per_query_score_list = []
    per_query_QV_list = []
    for line in fp.readlines():
        parts = line.split('\t')
        if qid == "" or parts[0] == qid:
            if count < topdocs:
                per_query_score_list.append(parts[3])
                qid = parts[0]
                count += 1
            else:
                # print('query : ', qid, '\t', per_query_score_list)
                per_query_score_list = sorted(per_query_score_list, reverse=True)
                gini = compute_gini_uqv(per_query_score_list, varscores)
                per_query_QV_list.append(gini)
                count = 1
                qid = parts[0]
                per_query_score_list = [parts[3]]
        elif parts[0] != qid:
            # print('query : ', qid, '\t', per_query_score_list)
            per_query_score_list = sorted(per_query_score_list, reverse=True)
            gini = compute_gini_uqv(per_query_score_list, varscores)
            per_query_QV_list.append(gini)
            uqv_g_Q[qid] = per_query_QV_list
            count = 1
            qid = parts[0]
            per_query_score_list = [parts[3]]
            per_query_QV_list = []
    # print('query : ', qid, '\t', per_query_score_list)
    per_query_score_list = sorted(per_query_score_list, reverse=True)
    gini = compute_gini_uqv(per_query_score_list, varscores)
    per_query_QV_list.append(gini)
    uqv_g_Q[qid] = per_query_QV_list
    # print("final list : ", uqv_g_Q)

# ================ calculate NQC_v : del_v(Q,Q') ==================

variance_trec_query(arg_trec_prerank_file, arg_top_docs_iq)
print("\nTREC res file variance dict : ", trec_v_Q)
variance_uqv_query(arg_uqv_prerank_file, arg_top_docs_vq, arg_top_scores_vq)
print("\nUQV res file variance dict : ", uqv_v_Q)


# # del_v_avg(Q,Q') = 1/n * \sum(v(Q')-v(Q)/v(Q))
# del_avg_Q = 0
# for key in trec_v_Q:
#     # print("key : ", key)
#     q_dash = uqv_v_Q[key]
#     # print("qdash : ", q_dash)
#     for val in q_dash:
#         del_avg_Q += (trec_v_Q[key] - val) / trec_v_Q[key]
#         # print("del v : ", del_avg_Q)
#     del_avg_Q = del_avg_Q / len(q_dash)
#     nqc_v_dict[key] = round(del_avg_Q, 4)
# print("\ndel_v_(Q,Q') : ", nqc_v_dict)


# del_v(Q,Q') = X(v(Q')) - v(Q) / v(Q) : X = {max, min, avg}
for key in trec_v_Q:
    # print("key : ", key)
    q_dash = uqv_v_Q[key]
    # print("qdash : ", q_dash)
    # max_v_Q_var = max(q_dash)
    # print("max(v(Q')) : ", max_v_Q_var)
    # min_v_Q_var = min(q_dash)
    # print("min(v(Q')) : ", min_v_Q_var)
    avg_v_Q_var = sum(q_dash) / len(q_dash)
    # print("avg(v(Q')) : ", avg_v_Q_var)
    # max_v_Q_var = (trec_v_Q[key] - max_v_Q_var) / trec_v_Q[key]
    # min_v_Q_var = trec_v_Q[key] - min_v_Q_var / trec_v_Q[key]
    avg_v_Q_var = (trec_v_Q[key] - avg_v_Q_var) / trec_v_Q[key]
    # avg_v_Q_var = (avg_v_Q_var - trec_v_Q[key]) / trec_v_Q[key]
    # nqc_v_dict[key] = round(max_v_Q_var, 4)
    # nqc_v_dict[key] = round(min_v_Q_var, 4)
    nqc_v_dict[key] = round(avg_v_Q_var, 4)
print("\ndel_v_(Q,Q') : ", nqc_v_dict)

# =============== compute rho & tau for NQC_v ====================

fp = open(arg_trec_ap_file)
ap_scores = []
nqc_v_scores = []
for line in fp.readlines():
    ap_scores.append(float(line.split('\t')[1]))
for key in nqc_v_dict:
    nqc_v_scores.append(nqc_v_dict[key])

xranks = pd.Series(ap_scores).rank()
# print("Rankings of X:", xranks)
yranks = pd.Series(nqc_v_scores).rank()
# print("Rankings of Y:", yranks)
rho, _ = stats.spearmanr(ap_scores, nqc_v_scores)
# print("\nSpearman's Rank correlation:", round(rho, 4))

tau, _ = stats.kendalltau(ap_scores, nqc_v_scores)
# print('Kendall Rank correlation: %.5f' % tau)

print(round(rho, 4), '\t', round(tau, 4))

# for qid, nqc_v in nqc_v_dict.items():
#     fw_variance.writelines(str(qid) + '\t' + str(nqc_v) + '\n')
# fw_variance.writelines('\n\n' + str(rho) + '\t' + str(tau))
# fw_variance.close()

# ================ calculate NQC_v : del_v(Q,Q') ==================

# gini_trec_query(arg_trec_prerank_file, arg_top_docs_iq)
# print("\nTREC res file gini dict : ", trec_g_Q)
# gini_uqv_query(arg_uqv_prerank_file, arg_top_docs_vq, arg_top_scores_vq)
# print("\nUQV res file gini dict : ", uqv_g_Q)
#
#
# # # del_v_avg(Q,Q') = 1/n * \sum(v(Q')-v(Q)/v(Q))
# # del_avg_Q = 0
# # for key in trec_g_Q:
# #     # print("key : ", key)
# #     q_dash = uqv_g_Q[key]
# #     # print("qdash : ", q_dash)
# #     for val in q_dash:
# #         del_avg_Q += (val - trec_g_Q[key]) / trec_g_Q[key]
# #         # print("del v : ", del_avg_Q)
# #     del_avg_Q = del_avg_Q / len(q_dash)
# #     nqc_g_dict[key] = round(del_avg_Q, 4)
# # print("\ndel_g_(Q,Q') : ", nqc_g_dict)
#
#
# # del_v(Q,Q') = X(v(Q')) - v(Q) / v(Q) : X = {max, min, avg}
# for key in trec_g_Q:
#     # print("key : ", key)
#     q_dash = uqv_g_Q[key]
#     # print("qdash : ", q_dash)
#     # max_g_Q_var = max(q_dash)
#     # print("max(v(Q')) : ", max_g_Q_var)
#     min_g_Q_var = min(q_dash)
#     # print("min(v(Q')) : ", min_g_Q_var)
#     # avg_g_Q_var = sum(q_dash) / len(q_dash)
#     # print("avg(v(Q')) : ", avg_g_Q_var)
#     # max_g_Q_var = (trec_g_Q[key] - max_v_Q_var) / trec_g_Q[key]
#     min_g_Q_var = (trec_g_Q[key] - min_g_Q_var) / trec_g_Q[key]
#     # avg_g_Q_var = (avg_g_Q_var - trec_g_Q[key]) / trec_g_Q[key]
#     # nqc_g_dict[key] = round(max_g_Q_var, 4)
#     # nqc_g_dict[key] = round(min_g_Q_var, 4)
#     # nqc_g_dict[key] = round(avg_g_Q_var, 4)
# print("\ndel_g_(Q,Q') : ", nqc_g_dict)
#
# # =============== compute rho & tau for NQC_v ====================
#
# nqc_g_scores = []
# for key in nqc_v_dict:
#     nqc_g_scores.append(nqc_g_dict[key])
#
# xranks = pd.Series(ap_scores).rank()
# # print("Rankings of X:", xranks)
# yranks = pd.Series(nqc_g_scores).rank()
# # print("Rankings of Y:", yranks)
# rho, _ = stats.spearmanr(ap_scores, nqc_g_scores)
# print("\nSpearman's Rank correlation:", round(rho, 4))
#
# tau, _ = stats.kendalltau(ap_scores, nqc_g_scores)
# print('Kendall Rank correlation: %.5f' % tau)
#
# # for qid, nqc_g in nqc_g_dict.items():
# #     fw_gini.writelines(str(qid) + '\t' + str(nqc_g) + '\n')
# # fw_gini.writelines('\n\n' + str(rho) + '\t' + str(tau))
# # fw_gini.close()