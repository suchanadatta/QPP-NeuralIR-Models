import sys
from math import sqrt, log
from nltk.stem import PorterStemmer
from gensim.parsing import remove_stopwords

if len(sys.argv) < 3:
    print('Needs 2 arguments - <LM / DRMM res file> <no. of top retrieved docs>')
    exit(0)

# arg_corpus_file = sys.argv[1]
# arg_topics_file = sys.argv[2]
# arg_lmres_file = sys.argv[3]
# arg_drmm_res_file = sys.argv[3]
# no_of_top_docs = sys.argv[4]

# for fast run
# arg_drmm_res_file = sys.argv[1]
arg_lmres_file = sys.argv[1]
no_of_top_docs = sys.argv[2]

stemmer = PorterStemmer()
collection_freq_dict = {}
document_freq_dict = {}
nqc_dict = {}
lm_nqc_dict = {}
drmm_nqc_dict = {}

# collec_freq_file = open('./collection_frequency.txt', 'w')
# doc_freq_file = open('./document_frequency.txt', 'w')
f_lm = open('/home/suchana/Desktop/' + no_of_top_docs + 'foo.res', 'w')
# f_drmm = open('/home/suchana/Desktop/foo.nqc', 'w')


def read_file(file):
    fp = open(file)
    output = {}
    for line in fp.readlines():
        parts = line.split(' ', 1)
        id = parts[0]
        text = parts[1]
        output[id] = text
    return output


def compute_collection_size(doc_dict):
    vocab_size = 0
    for id, doc in doc_dict.items():
        vocab_size += len(doc.split())
    return vocab_size


def compute_collection_frequency(query_dict, doc_dict):
    for qno, query in query_dict.items():
        for qterm in remove_stopwords(query).split():
            term_count = 0
            qterm_stem = stemmer.stem(qterm.lower().strip())
            # print('qterm : ', qterm_stem)
            for docid, doc in doc_dict.items():
                for term in doc.split():
                    if term == qterm_stem:
                        term_count += 1
            # print('term count : ', qterm_stem, '\t', term_count)
            collection_freq_dict[qterm_stem] = term_count
    return collection_freq_dict


def compute_document_frequency(query_dict, doc_dict):
    for qno, query in query_dict.items():
        for qterm in remove_stopwords(query).split():
            qterm_stem = stemmer.stem(qterm.lower().strip())
            print('qterm : ', qterm_stem)
            for docid, doc in doc_dict.items():
                flag = 1
                for term in doc.split():
                    if term == qterm_stem and flag == 1 and document_freq_dict.get(term) != 0:
                        if document_freq_dict.get(term) is None:
                            document_freq_dict[term] = 0
                        document_freq_dict[term] += 1
                        flag = 0
            document_freq_dict[term] = 0
            print('doc freq : ', qterm_stem, '\t', document_freq_dict[qterm_stem])
    return document_freq_dict


def compute_mean(per_query_score_list):
    sum_score = 0
    for score_doc in per_query_score_list:
        sum_score += float(score_doc)
    # print('sum : ', sum_score)
    mean = sum_score * (1 / int(no_of_top_docs))
    # print('mean : ', mean)
    return mean


# def compute_collection_score_CF(qid):  # calculate the factor 1/score(D) using collection frequency of the query term
#     collection_score_cf = 0
#     for qno, query in query_dict.items():
#         if qid == qno:
#             for qterm in remove_stopwords(query).split():
#                 qterm_stem = stemmer.stem(qterm.lower().strip())
#                 # print('qterm : ', qterm_stem)
#                 for term, freq in collection_freq_dict.items():
#                     if term == qterm_stem:
#                         y = float(freq) / collection_size
#                         # print('freq :', freq)
#                         # print('collec size : ', collection_size)
#                         # print('y : ', y)
#                         collection_score_cf += log(1 + y)
#                         # print('col score : ', collection_score_cf)
#                         # collection_score += log(1 + y, 10)
#                         # print('col score : ', collection_score_cf)
#             # print('tot col score : ', collection_score_cf)
#     return collection_score_cf


# def compute_collection_score_DF(qid):  # calculate the factor 1/score(D) using document frequency of the query term
#     collection_score_df = 0
#     for qno, query in query_dict.items():
#         if qid == qno:
#             for qterm in remove_stopwords(query).split():
#                 qterm_stem = stemmer.stem(qterm.lower().strip())
#                 # print('qterm : ', qterm_stem)
#                 for term, freq in document_freq_dict.items():
#                     if term == qterm_stem:
#                         y = len(doc_dict) / freq
#                         print('freq :', freq)
#                         print('collec size : ', len(doc_dict))
#                         print('y : ', y)
#                         collection_score_df += log(y)
#             print('tot col score : ', collection_score_df)
#     return collection_score_df


def nqc_pos_neg(per_query_score_list, mu, qid):
    nqc_pos = 0
    nqc_neg = 0
    # print('qid : ', qid)
    # collection_score_cf = compute_collection_score_CF(qid)
    # print('coll score : ', collection_score_cf)
    # collection_score_df = compute_collection_score_DF(qid)
    # print('coll score : ', collection_score_df)
    for value in per_query_score_list:
        if float(value) < mu:
            # print('value : ', value)
            nqc_neg += pow((float(value) - mu), 2)
            # print('nqc_neg : ', nqc_neg)
        else:
            # print('here value : ', value)
            nqc_pos += pow((float(value) - mu), 2)
            # print('nqc_pos : ', nqc_pos)
    # nqc_neg = sqrt(nqc_neg * (1 / int(no_of_top_docs))) * (1 / collection_score_cf)
    # nqc_neg = sqrt(nqc_neg * (1 / int(no_of_top_docs))) * collection_score_df
    nqc_neg = sqrt(nqc_neg * (1 / int(no_of_top_docs)))
    # print('NQC-neg : ', nqc_neg)
    # nqc_pos = sqrt(nqc_pos * (1 / int(no_of_top_docs))) * (1 / collection_score_cf)
    # nqc_pos = sqrt(nqc_pos * (1 / int(no_of_top_docs))) * collection_score_df
    nqc_pos = sqrt(nqc_pos * (1 / int(no_of_top_docs)))
    # print('NQC-pos : ', nqc_pos)
    final_nqc = sqrt(pow(nqc_pos, 2) + pow(nqc_neg, 2))
    # print('final nqc : ', final_nqc)
    nqc_dict[qid] = final_nqc
    # print('dict : ', nqc_dict)


def nqc_full(per_query_score_list, mu, qid):
    nqc = 0
    # print('qid : ', qid)
    # collection_score_cf = compute_collection_score_CF(qid)
    # print('coll score : ', collection_score_cf)
    # collection_score_df = compute_collection_score_DF(qid)
    # print('coll score : ', collection_score_df)
    for value in per_query_score_list:
        if float(value) < mu:
            nqc += pow((float(value) - mu), 2)
    nqc = sqrt(nqc * (1 / int(no_of_top_docs)))
    nqc_dict[qid] = round(nqc, 4)
    # print('dict : ', nqc_dict)


def calculate_nqc(res_file, top_docs):
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
            print('query : ', qid, '\t', per_query_score_list)
            mu = compute_mean(per_query_score_list)
            # nqc_pos_neg(per_query_score_list, mu, qid)
            nqc_full(per_query_score_list, mu, qid)
            per_query_score_list = []
            count = 0
            qid = parts[0]
            score = parts[4]
            per_query_score_list.append(score)
            count = count + 1
    print('query : ', qid, '\t', per_query_score_list)
    mu = compute_mean(per_query_score_list)
    # nqc_pos_neg(per_query_score_list, mu, qid)
    nqc_full(per_query_score_list, mu, qid)


# doc_dict = read_file(arg_corpus_file)
# print('doc_dict size : ', len(doc_dict))
# query_dict = read_file(arg_topics_file)
# print('query dict size : ', len(query_dict))
# collection_size = compute_collection_size(doc_dict)
# print('collection size : ', collection_size)

# collection_freq_dict = compute_collection_frequency(query_dict, doc_dict)
# for term, col_freq in collection_freq_dict.items():
#     collec_freq_file.writelines(term + ' ' + str(col_freq) + '\n')
# collec_freq_file.close()
# collection_freq_dict = read_file("./trec_query_term_collec_freq")   # read qTerm CF externally
# print('collection freq dict : ', collection_freq_dict)

# document_freq_dict = compute_document_frequency(query_dict, doc_dict)
# for term, doc_freq in document_freq_dict.items():
#     doc_freq_file.writelines(term + ' ' + str(doc_freq) + '\n')
# doc_freq_file.close()
# document_freq_dict = read_file('./document_frequency.txt')   # read qTerm DF externally
# print('document freq dict : ', document_freq_dict)

calculate_nqc(arg_lmres_file, int(no_of_top_docs))
lm_nqc_dict = nqc_dict.copy()
print('dict : ', lm_nqc_dict)
for qid, nqc_val in lm_nqc_dict.items():
    f_lm.writelines(str(qid) + '\t' + str(nqc_val) + '\n')
f_lm.close()
# nqc_dict.clear()
# calculate_nqc(arg_drmm_res_file, int(no_of_top_docs))
# drmm_nqc_dict = nqc_dict.copy()
# print('dict : ', drmm_nqc_dict)
# for qid, nqc_val in drmm_nqc_dict.items():
#     f_drmm.writelines(str(qid) + '\t' + str(nqc_val) + '\n')
# f_drmm.close()
