import os
import numpy as np

max_doclen = 100
query_term_maxlen = 5

#
# loads the qrels rel-nonrel train fold file, + translation matrix data, returns keras ready numpy input, + empty labels
#
def get_keras_train_input(pair_file, similarity_matrix_file):

    topic_rel_nonrel = []
    with open(pair_file, 'r') as inputFile:
        for line in inputFile:
            parts = line.strip().split()
            topic_rel_nonrel.append((parts[0], parts[1], parts[2]))
    print('loaded ' + str(len(topic_rel_nonrel)) + ' qrel pair entries')

    similarity_data, similarity_count = load_similarity_data(similarity_matrix_file)

    #
    # create numpy arrays
    #
    # the loss function needs a round number, * 2 because we have two input lines for every pair
    data_count = int(len(topic_rel_nonrel) / 10) * 10 * 2
    print('data count : ', data_count)

    # np similarity
    similarity_input = np.zeros((data_count, query_term_maxlen, max_doclen), dtype=np.float32)

    # empty label array
    labels = np.zeros((data_count,), dtype=np.int32)
    labels[::2] = 1

    i_input = 0
    skipped_count = 0
    #
    # for every line here create 2 numpy lines, first line is relevant doc, second line is non_relevant
    #
    for i_output in range(0, data_count, 2):

        topic, rel_doc, nonrel_doc = topic_rel_nonrel[i_input]
        i_input += 1

        # there might be one or two pairs not in the similarity matrix data - ignore them for now
        if topic in similarity_data and rel_doc in similarity_data[topic] and nonrel_doc in similarity_data[topic]:

            topic_rel_data = similarity_data[topic][rel_doc]
            topic_nonrel_data = similarity_data[topic][nonrel_doc]

            # similarity
            for w in range(len(topic_rel_data[2])):  # same topic -> therefore same similarity count
                similarity_input[i_output][w] = topic_rel_data[2][w]  # np.ones(100,dtype=np.float32)
                similarity_input[i_output + 1][w] = topic_nonrel_data[2][w]  # np.zeros(100,dtype=np.float32)
        else:
            skipped_count += 1

    print("similarity_input:", similarity_input.shape)
    print("skipped_count:", skipped_count)

    return {'doc': similarity_input}, labels


#
# loads the pre-ranked test fold file, + similarity data, returns keras ready numpy input + prerank data
#
def get_keras_test_input(preranked_file, prerank_similarity_matrix):
    topic_prerank = []
    with open(preranked_file, 'r') as inputFile:
        for line in inputFile:
            parts = line.strip().split()
            topic_prerank.append((parts[0], parts[1]))

    print('loaded ' + str(len(topic_prerank)) + ' prerank entries')

    similarity_data, similarity_count = load_similarity_data(prerank_similarity_matrix)

    #
    # create numpy arrays
    #
    data_count = len(topic_prerank)

    # np histogram
    similarity_input = np.zeros((data_count, query_term_maxlen, max_doclen), dtype=np.float32)

    i_input = 0
    skipped_count = 0

    for i_output in range(0, data_count, 1):
        topic, rel_doc = topic_prerank[i_input]
        i_input += 1

        # there might be one or two pairs not in the histogram data - ignore them for now
        if topic in similarity_data and rel_doc in similarity_data[topic]:
            topic_rel_data = similarity_data[topic][rel_doc]

            # similarity
            for w in range(len(topic_rel_data[2])):  # same topic -> therefore same cosim count
                similarity_input[i_output][w] = topic_rel_data[2][w]  # np.ones(100,dtype=np.float32
        else:
            skipped_count += 1

    print("similarity_input:", similarity_input.shape)
    print("skipped_count:", skipped_count)

    return {'doc': similarity_input}, topic_prerank


def load_similarity_data(filepath):

    print('Max document length : ', max_doclen)
    data_per_topic = {}  # topic -> [np.array(cosim)])

    ignore_docs = ["315", "340", "601", "632", "652", "684"]

    count = 0
    with open(filepath, 'r') as inputFile:
        for line in inputFile:
            count += 1
            parts = line.strip().split()
            # histogram file format: topicId DocId relscore numberOfTopicWords(N) <cosim1> <cosim2> ... <cosimN>
            topicId = parts[0]
            docId = parts[1]
            score = float(parts[2])

            if topicId not in ignore_docs:
                similarity_matrix = []
                for i in range(4, len(parts), max_doclen):
                    cosim = []
                    for t in range(0, max_doclen):
                        cosim.append(float(parts[i + t]))
                        print('found cosim',float(parts[i + t]),' at ',t,' for topic ',topicId, docId)
                    similarity_matrix.append(np.array(cosim, np.float32))

                if topicId not in data_per_topic:
                    data_per_topic[topicId] = {}

                data_per_topic[topicId][docId] = (score, similarity_matrix)

    print('loaded ' + str(count) + ' topic<->doc cosine-similarity entries')
    return data_per_topic, count
