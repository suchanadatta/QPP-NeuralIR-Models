import sys
import re
from builtins import round
from statistics import mean
import xml.etree.ElementTree as ET
from gensim.parsing import remove_stopwords
from nltk.stem import PorterStemmer
import numpy as np
import pandas as pd
from scipy import stats


if len(sys.argv) < 11:
    print('Needs 10 arguments - \n1. TREC initial query based LM reranked file (reranked by DRMM)\n'
          '2. UQV-TREC query variants based LM reranked file (reranked by DRMM)\n'
          '3. TREC initial query .AP file\n'
          '4. TREC query file\n'
          '5. Query variant file (UQV queries)\n'
          '6. res file path\n'
          '7. No. of top documents you want to take from the initial.res file (retrieved by initial query)\n'
          '8. No. of top documents retrieved by query variant in the variant.res file (generated by LM and '
          're-ranked by DRMM)\n'
          '9. No. of top scores you want to consider for each variant\n'
          '10. Value of qmix [0.1-0.9]')
    exit(0)

arg_trec_prerank_file = sys.argv[1]
arg_uqv_prerank_file = sys.argv[2]
arg_trec_ap_file = sys.argv[3]
arg_trec_query_file = sys.argv[4]
arg_query_variant_file = sys.argv[5]
arg_res_path = sys.argv[6]
arg_top_docs_iq = int(sys.argv[7])
arg_top_docs_vq = int(sys.argv[8])
arg_top_scores_vq = int(sys.argv[9])
arg_qmix = float(sys.argv[10])

# fw_variance = open(arg_res_path + 'TD-' + str(arg_top_docs_iq) + 'TS-' + str(arg_top_docs_vq) +
#                    '-qmix-' + str(arg_qmix) + '_variance.res', 'w')
# fw_gini = open(arg_res_path + 'TD-' + str(arg_top_docs_iq) + 'TS-' + str(arg_top_docs_vq) +
#                '-qmix-' + str(arg_qmix) + '_gini.res', 'w')

query_similarity = {}
trec_r_Q = {}
uqv_r_Q = {}
nqc_r_dict = {}


def compute_regression_trec(score_list, qid):
    doc_rank = np.arange(1, len(score_list)+1, 1)
    # print('doc rank :', doc_rank)
    score_list = np.array(score_list).astype(np.float)
    # print('score list : ', score_list)
    # print('shape of score list : ', score_list.shape)
    slop = (((mean(doc_rank) * mean(score_list)) - mean(doc_rank * score_list)) /
            ((mean(doc_rank) * mean(doc_rank)) - mean(doc_rank * doc_rank)))
    # print('slop : ', slop)
    intercept = mean(score_list) - slop * mean(doc_rank)
    # print('intercept : ', intercept)
    trec_r_Q[qid] = round(abs(slop), 4)


def regression_trec_query(trec_res_file, topdocs):
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
            compute_regression_trec(per_query_score_list, qid)
            per_query_score_list = []
            count = 0
            qid = parts[0]
            score = parts[4]
            per_query_score_list.append(score)
            count = count + 1
    # print('query : ', qid, '\t', per_query_score_list)
    compute_regression_trec(per_query_score_list, qid)


def compute_regression_uqv(score_list, varscores):
    # print("sorted list : ", score_list)
    score_list = np.array(score_list).astype(np.float)
    score_list = score_list[0:varscores]
    # print('sub-score list : ', score_list)
    doc_rank = np.arange(1, len(score_list) + 1, 1)
    # print('doc rank :', doc_rank)
    slop = (((mean(doc_rank) * mean(score_list)) - mean(doc_rank * score_list)) /
            ((mean(doc_rank) * mean(doc_rank)) - mean(doc_rank * doc_rank)))
    # print('slop : ', slop)
    intercept = mean(score_list) - slop * mean(doc_rank)
    # print('intercept : ', intercept)
    return round(abs(slop), 6)


def regression_uqv_query(uqv_res_file, topdocs, varscores):
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
                regression = compute_regression_uqv(per_query_score_list, varscores)
                per_query_QV_list.append(regression)
                count = 1
                qid = parts[0]
                per_query_score_list = [parts[4]]
        elif parts[0] != qid:
            # print('query : ', qid, '\t', 'score list size : ', len(per_query_score_list))
            per_query_score_list = sorted(per_query_score_list, reverse=True)
            regression = compute_regression_uqv(per_query_score_list, varscores)
            per_query_QV_list.append(regression)
            uqv_r_Q[qid] = per_query_QV_list
            # print('query : ', qid, '\t', 'no. of query variants : ', len(per_query_QV_list))
            count = 1
            qid = parts[0]
            per_query_score_list = [parts[4]]
            per_query_QV_list = []
    # print('query : ', qid, '\t', 'score list size : ', len(per_query_score_list))
    per_query_score_list = sorted(per_query_score_list, reverse=True)
    regression = compute_regression_uqv(per_query_score_list, varscores)
    per_query_QV_list.append(regression)
    uqv_r_Q[qid] = per_query_QV_list
    # print('query : ', qid, '\t', 'no. of query variants : ', len(per_query_QV_list))
    # print("final list : ", uqv_r_Q)

# =============== compute inter-query association p'(q'|q) ==============


def jaccard_similarity(initial_dict, var_dict):
    stemmer = PorterStemmer()
    for qid in initial_dict:
        similarity_list = []
        initial = remove_stopwords(initial_dict[qid])
        initial_stem = stemmer.stem(initial.lower().strip())
        initial_set = set(initial_stem.split())
        # print("initial set : ", initial_set)
        variant_list = var_dict[qid]
        # print("var list : ", variant_list)
        for var in variant_list:
            # print("one var : ", var)
            variant = remove_stopwords(var)
            variant_stem = stemmer.stem(variant.lower().strip())
            variant_set = set(variant_stem.split())
            # print("var set : ", variant_set)
            intersec = initial_set.intersection(variant_set)
            # print("intersection : ", intersec)
            similarity = round(float(len(intersec)) / (len(initial_set) + len(variant_set) - len(intersec)), 4)
            # print("similarity : ", similarity)
            similarity_list.append(similarity)
        query_similarity[qid] = np.array(similarity_list).astype(float)
    # print("inter query similarity : ", query_similarity)


def inter_query_association_uqv(initial_query, query_variants):
    initial_query_dict = {}
    variant_dict = {}
    rootElement = ET.parse(initial_query).getroot()
    for subElement in rootElement:
        query = re.sub('[^a-zA-Z0-9\n\.]', ' ', subElement[1].text)
        initial_query_dict[subElement[0].text.strip()] = query
    # print(initial_query_dict)

    fp = open(query_variants)
    qid = ''
    per_query_var_list = []
    for line in fp.readlines():
        parts = line.split('-')
        if qid == '' or parts[0] == qid:
            qid = parts[0]
            variant = parts[2].split(';')
            variant = variant[1].replace('\n', '')
            variant_clean = re.sub('[^a-zA-Z0-9\n\.]', ' ', variant)
            # print(variant_clean)
            per_query_var_list.append(variant_clean)
        elif parts[0] != qid:
            variant_dict[qid] = per_query_var_list
            qid = parts[0]
            variant = parts[2].split(';')
            variant = variant[1].replace('\n', '')
            variant_clean = re.sub('[^a-zA-Z0-9\n\.]', ' ', variant)
            # print(variant_clean)
            per_query_var_list = [variant_clean]
    variant_dict[qid] = per_query_var_list
    # print(variant_dict)
    jaccard_similarity(initial_query_dict, variant_dict)


def inter_query_association_dsd(initial_query, query_variants):
    initial_query_dict = {}
    variant_dict = {}
    rootElement = ET.parse(initial_query).getroot()
    for subElement in rootElement:
        query = re.sub('[^a-zA-Z0-9\n\.]', ' ', subElement[1].text)
        initial_query_dict[subElement[0].text.strip()] = query
    # print(initial_query_dict)

    fp = open(query_variants)
    qid = ''
    per_query_var_list = []
    for line in fp.readlines():
        parts = line.split('\t')
        if qid == '' or parts[0] == qid:
            qid = parts[0]
            variant = parts[1].replace('\n', '')
            variant_clean = re.sub('[^a-zA-Z0-9\n\.]', ' ', variant)
            # print(variant_clean)
            per_query_var_list.append(variant_clean)
        elif parts[0] != qid:
            variant_dict[qid] = per_query_var_list
            qid = parts[0]
            variant = parts[1].replace('\n', '')
            variant_clean = re.sub('[^a-zA-Z0-9\n\.]', ' ', variant)
            # print(variant_clean)
            per_query_var_list = [variant_clean]
    variant_dict[qid] = per_query_var_list
    # print(variant_dict)
    jaccard_similarity(initial_query_dict, variant_dict)


# inter_query_association_uqv(arg_trec_query_file, arg_query_variant_file)  # for UQV (manual query variants)
inter_query_association_dsd(arg_trec_query_file, arg_query_variant_file)  # for DSD (our variants obtained using RM and W2V)

# ================ calculate NQC_v : del_avg(Q,Q') = del_v(Q') - del_v(Q) / del_v(Q) ==================

regression_trec_query(arg_trec_prerank_file, arg_top_docs_iq)
# print("\nTREC res file variance dict : ", trec_r_Q)
regression_uqv_query(arg_uqv_prerank_file, arg_top_docs_vq, arg_top_scores_vq)
# print("\nUQV res file variance dict : ", uqv_v_Q)

only_ref = 0
for key in trec_r_Q:
    # print("\nkey : ", key)
    q_dash = uqv_r_Q[key]
    # print("qdash : ", q_dash)
    similarity = query_similarity[key]
    # print("similarity list : ", similarity)
    res_list = []
    for i in range(0, len(q_dash)):
        res_list.append(q_dash[i] * similarity[i])
    only_ref = sum(res_list) / len(q_dash)
    # print("only ref : ", only_ref)
    only_ref = arg_qmix * trec_r_Q[key] + (1 - arg_qmix) * only_ref
    # print("now only ref : ", only_ref)
    nqc_r_dict[key] = round(only_ref, 4)
print("\nP_onlyref(Q) : ", nqc_r_dict)
#
# # =============== compute rho & tau for NQC_v ====================

fp = open(arg_trec_ap_file)
ap_scores = []
nqc_v_scores = []
for line in fp.readlines():
    ap_scores.append(float(line.split('\t')[1]))
for key in nqc_r_dict:
    nqc_v_scores.append(nqc_r_dict[key])

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