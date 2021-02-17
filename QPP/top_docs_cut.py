import csv

tsv_file = open("/store/causalIR/drmm/NQC_trec/query_variants/trec-8_queries.xml-LMDirichlet1000.0-TD10-W2V_v30.variants.uniq", "r")
read_tsv = csv.reader(tsv_file, delimiter="\t")
f = open("/store/causalIR/drmm/NQC_trec/query_variants/trec-8_queries.xml-LMDirichlet1000.0-TD10-W2V_v25.variants.uniq", "w")

#  file consists of top ret n docs for each query and i want to cut top 100 docs for each query
qid = ""
count = 0
for line in read_tsv:
    # parts = line.split('\t')
    if qid == "" or line[0] == qid:
        if count < 25:
            qid = line[0]
            # score = line[3]
            variant = line[1]
            # f.writelines(line[0] + "\t" + line[1] + "\t" + line[2] + "\t" + line[3] + "\t" + line[4] + "\t" + line[5] + "\n")
            # f.writelines(line[0] + "\t" + line[1] + "\t" + line[2] + "\t" + str(count+1) + "\t" + line[3] + "\t" + line[4] + "\n")
            f.writelines(line[0] + "\t" + line[1] + "\n")
            count = count + 1
    elif line[0] != qid:
        count = 0
        qid = line[0]
        # score = line[3]
        variant = line[1]
        # f.writelines(line[0] + "\t" + line[1] + "\t" + line[2] + "\t" + line[3] + "\t" + line[4] + "\t" + line[5] + "\n")
        # f.writelines(line[0] + "\t" + line[1] + "\t" + line[2] + "\t" + str(count+1) + "\t" + line[3] + "\t" + line[4] + "\n")
        f.writelines(line[0] + "\t" + line[1] + "\n")
        count = count + 1
f.close()

# file consists of top ret n docs for each query variants and i want to write them in TREC format
# qid = ""
# count = 1
# for line in read_tsv:
#     # parts = line.split('\t')
#     if count < 100:
#         f.writelines(line[0] + "\t" + line[1] + "\t" + line[2] + "\t" + str(count) + "\t" + line[3] + "\t" + line[4] + "\n")
#         count = count + 1
#     else:
#         f.writelines(line[0] + "\t" + line[1] + "\t" + line[2] + "\t" + str(count) + "\t" + line[3] + "\t" + line[4] + "\n")
#         count = 1
#     # elif line[0] != qid:
#     #     count = 0
#     #     qid = line[0]
#     #     score = line[4]
#     #     # f.writelines(line[0] + "\t" + line[1] + "\t" + line[2] + "\t" + line[3] + "\t" + line[4] + "\t" + line[5] + "\n")
#     #     f.writelines(line[0] + "\t" + line[1] + "\t" + line[2] + "\t" + str(count+1) + "\t" + line[3] + "\t" + line[4] + "\n")
#     #     count = count + 1
# f.close()


# file consists of top ret n docs for each query variants and i want to cut n-m lines for each query variant
# ret_cut = 100
# variant_cut = 5
# count = 1
# score_list = []
# for line in read_tsv:
#     if count <= variant_cut:
#         print(line)
#         count += 1
#     elif count < ret_cut:
#         count += 1
#     else:
#         count = 1