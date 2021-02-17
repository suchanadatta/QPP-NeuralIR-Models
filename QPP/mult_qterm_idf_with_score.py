# baseline for Model-agnostic approach
# multiple qterm average idf with the DRMM retrieval scores
# i/p -> prerank_histogram file
#     -> drmm score.res file
# o/p -> drmm_score.res file, where score = score * avg idf of query terms

import sys

if len(sys.argv) < 4:
    print('Needs 3 arguments - <DRMM-query varianta res file> <query-avg idf file> <final score file path>')
    exit(0)

arg_drmm_QV_file = sys.argv[1]
arg_avg_idf_file = sys.argv[2]
arg_res_file = sys.argv[3]

res_file = open(arg_res_file + 'trec-8_drmmW2V_with_idf.res', 'w')

qterm_idf_dict = {}
qid_list = list(range(401, 451, 1))
# print('qid list : ', qid_list)

def make_qterm_idf_dict(avg_idf_file):
    qid = ""
    per_query_idf_list = []
    fp = open(avg_idf_file)
    for line in fp.readlines():
        parts = line.split('\t')
        if qid == "" or parts[0] == qid:
            per_query_idf_list.append(round(float(parts[2]), 4))
            qid = parts[0]
        else:
            # print('###### : ', per_query_idf_list)
            qterm_idf_dict[qid] = per_query_idf_list
            qid = parts[0]
            per_query_idf_list = []
            per_query_idf_list.append(round(float(parts[2]), 4))
            # print('%%%% : ', per_query_idf_list)
        qterm_idf_dict[qid] = per_query_idf_list
    print('DICT : ', qterm_idf_dict)

def compute_final_scores(drmm_qv_file):
    qid = ""
    count = 0
    qv_no = 0
    idf_list = []
    fp = open(drmm_qv_file)
    for line in fp.readlines():
        parts = line.split('\t')
        if qid == "" or parts[0] != qid:
            count = 0
            qv_no = 0
            print('%%%%% : ', parts[0])
            idf_list = qterm_idf_dict[parts[0]]
            print('@@@@ : ', idf_list)
            qid = parts[0]
            if count < 100:
                res_file.write(parts[0] + '\t' + parts[1] + '\t' + parts[2] + '\t' + str(count+1) + '\t' + str(idf_list[qv_no] * float(parts[3])) + '\t' + parts[4])
                count = count + 1
        elif count < 100:
                res_file.write(parts[0] + '\t' + parts[1] + '\t' + parts[2] + '\t' + str(count+1) + '\t' + str(idf_list[qv_no] * float(parts[3])) + '\t' + parts[4])
                count = count + 1
        else:
            count = 0
            qv_no = qv_no + 1
            res_file.write(parts[0] + '\t' + parts[1] + '\t' + parts[2] + '\t' + str(count+1) + '\t' + str(idf_list[qv_no] * float(parts[3])) + '\t' + parts[4])
            count = count + 1

make_qterm_idf_dict(arg_avg_idf_file)
compute_final_scores(arg_drmm_QV_file)
res_file.close()
