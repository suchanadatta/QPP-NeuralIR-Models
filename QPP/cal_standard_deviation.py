import sys
from math import sqrt, log
from nltk.stem import PorterStemmer
from gensim.parsing import remove_stopwords

if len(sys.argv) < 3:
    print('Needs 2 arguments - <LM / DRMM res file> <no. of top retrieved docs>')
    exit(0)


arg_lmres_file = sys.argv[1]
no_of_top_docs = sys.argv[2]

std_dev_dict = {}


def read_file(file):
    fp = open(file)
    output = {}
    for line in fp.readlines():
        parts = line.split(' ', 1)
        id = parts[0]
        text = parts[1]
        output[id] = text
    return output


def compute_mean(per_query_score_list):
    sum_score = 0
    for score_doc in per_query_score_list:
        sum_score += float(score_doc)
    # print('sum : ', sum_score)
    mean = sum_score * (1 / int(no_of_top_docs))
    # print('mean : ', mean)
    return mean


def std_dev(per_query_score_list, mu, qid):
    stdev = 0
    for value in per_query_score_list:
        if float(value) < mu:
            stdev += pow((float(value) - mu), 2)
    stdev = sqrt(stdev * (1 / int(no_of_top_docs)))
    std_dev_dict[qid] = round(stdev, 4)


def calculate_std_dev(res_file, top_docs):
    qid = ""
    count = 0
    per_query_score_list = []
    fp = open(res_file)
    for line in fp.readlines():
        parts = line.split('\t')
        if qid == "" or parts[0] == qid:
            if count < top_docs:
                qid = parts[0]
                score = parts[4]
                per_query_score_list.append(score)
                count = count + 1
        elif parts[0] != qid:
            # print('query : ', qid, '\t', per_query_score_list)
            mu = compute_mean(per_query_score_list)
            # nqc_pos_neg(per_query_score_list, mu, qid)
            std_dev(per_query_score_list, mu, qid)
            per_query_score_list = []
            count = 0
            qid = parts[0]
            score = parts[4]
            per_query_score_list.append(score)
            count = count + 1
    # print('query : ', qid, '\t', per_query_score_list)
    mu = compute_mean(per_query_score_list)
    # nqc_pos_neg(per_query_score_list, mu, qid)
    std_dev(per_query_score_list, mu, qid)

calculate_std_dev(arg_lmres_file, int(no_of_top_docs))
# print('the dict final : ', std_dev_dict)
for key in std_dev_dict:
    print(key, '\t', std_dev_dict[key])