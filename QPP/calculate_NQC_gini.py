import sys
import numpy as np

if len(sys.argv) < 3:
    print('Needs 2 arguments - <LM / DRMM res file> <no. of top retrieved docs>')
    exit(0)

arg_lmres_file = sys.argv[1]
no_of_top_docs = sys.argv[2]

f_lm = open('/home/suchana/NQC_recompute/DRMM_NQC_noQV/k_cut_nqc_g/drmm_' + no_of_top_docs + '.gini', 'w')
gini_dict = {}


def gini(per_query_score_list, qid):
    weighted_sum = 0
    i = 1
    gini_array = np.array(per_query_score_list).astype(np.float)
    gini_array.sort()
    print(gini_array)
    gini_array_size = gini_array.size
    print(gini_array_size)
    coef = 2 / gini_array_size
    print(coef)
    const = (gini_array_size + 1) / gini_array_size
    print(const)
    while i <= gini_array_size:
        for yi in gini_array:
            weighted_sum += i * yi
            i += 1
    print(weighted_sum)
    gini = coef * weighted_sum / (gini_array.sum()) - const
    print("gini coeff : ", gini)
    gini_dict[qid] = round(gini, 4)


def calculate_nqc_gini(res_file, top_docs):
    qid = ""
    count = 0
    per_query_score_list = []
    fp = open(res_file)
    for line in fp.readlines():
        parts = line.split('\t')
        if qid == "" or parts[0] == qid:
            if count < top_docs:
                qid = parts[0]
                score = parts[3]
                per_query_score_list.append(score)
                count = count + 1
        elif parts[0] != qid:
            print('query : ', qid, '\t', per_query_score_list)
            gini(per_query_score_list, qid)
            per_query_score_list = []
            count = 0
            qid = parts[0]
            score = parts[3]
            per_query_score_list.append(score)
            count = count + 1
    print('query : ', qid, '\t', per_query_score_list)
    gini(per_query_score_list, qid)


calculate_nqc_gini(arg_lmres_file, int(no_of_top_docs))
print('gini dict : ', gini_dict)
for qid, gini_val in gini_dict.items():
    f_lm.writelines(str(qid) + '\t' + str(gini_val) + '\n')
f_lm.close()

