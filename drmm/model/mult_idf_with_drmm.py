# baseline for Model-agnostic approach
# multiple qterm average idf with the DRMM retrieval scores
# i/p -> prerank_histogram file
#     -> drmm score.res file
# o/p -> drmm_score.res file, where score = score * avg idf of query terms

import sys

if len(sys.argv) < 4:
    print('Needs 3 arguments - <DRMM/LM res file> <prerank histogram file> <final score file path>')
    exit(0)

arg_drmm_file = sys.argv[1]
arg_hist_file = sys.argv[2]
arg_res_file = sys.argv[3]

res_file = open(arg_res_file + 'trec-8_lmdir_with_idf.res', 'w')

qterm_idf_dict = {}
qid_list = list(range(401, 451, 1))
# print('qid list : ', qid_list)

def make_qterm_idf_dict(hist_file):
    fp = open(hist_file)
    for line in fp.readlines():
        parts = line.strip().split()
        qid = int(parts[0])
        if qid in qid_list:
            no_of_qterms = int(parts[3])
            div = float(parts[3])
            idf_sum = 0.
            while no_of_qterms > 0:
                idf_sum += float(parts[3 + no_of_qterms])
                no_of_qterms = no_of_qterms - 1
            if qid not in qterm_idf_dict:
                qterm_idf_dict[qid] = round(idf_sum / div, 4)

def create_final_score(drmm_file):
    fp = open(drmm_file)
    for line in fp.readlines():
        parts = line.strip().split()
        qid = int(parts[0])
        score = round(float(parts[4]) * qterm_idf_dict[qid], 4)
        res_file.write(parts[0] + '\t' + parts[1] + '\t' + parts[2] + '\t' + parts[3] +'\t' + str(score) + '\t' + parts[5] + '\n')
    res_file.close()

make_qterm_idf_dict(arg_hist_file)
print('qterm idf dict : ', qterm_idf_dict)

create_final_score(arg_drmm_file)
