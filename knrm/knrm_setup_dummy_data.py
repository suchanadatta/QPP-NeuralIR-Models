"""ConvKNRM model."""

import keras
import tensorflow as tf
import numpy as np
from keras.layers import Input
from loss_function import rank_hinge_loss


def load_similarity_data(filepath):

    max_doc_len = 20
    data_per_line = {}  # topic -> [np.array(cosim)])

    count = 0
    with open(filepath, 'r') as inputFile:
        for line in inputFile:
            count += 1
            parts = line.strip().split()
            # similarity file format: topicId <cosim1> <cosim2> ... <cosimN>
            topicId = parts[0]
            #
            # handle similarity data
            #
            similarity_data = []
            for i in range(1, len(parts), max_doc_len):
                cosim = []
                for t in range(0, max_doc_len):
                    cosim.append(int(parts[i + t]))
                    print('found cosim',int(parts[i + t]),' at ',t,' for topic ',topicId)
                similarity_data.append(np.array(cosim, np.float32))

            if topicId not in data_per_line:
                data_per_line[topicId] = {}

            data_per_line[topicId] = similarity_data

    print('loaded ' + str(count) + ' topic <-> cosim entries')
    return data_per_line, count


def get_train_input(similarity_matrix_file):

    similarity_data, similarity_count = load_similarity_data(similarity_matrix_file)
    # print('sim data : ', similarity_data)

    #
    # create numpy arrays
    #

    # np similarity
    similarity_input = np.zeros((100, 3, 20), dtype=np.float32)
    print('similarity input : ', similarity_input)

    # empty label array
    labels = np.zeros((100,), dtype=np.int32)
    labels[::2] = 1
    print('labels : ', labels)

    #
    # for every line here create 2 numpy lines, first line is relevant doc, second line is non_relevant
    #
    for i_output in range(1, len(similarity_data)+1):
        print('i-output : ', i_output)
        topic_rel_data = similarity_data[str(i_output)]
        print('topic rel data : ', topic_rel_data)

        # similarity
        for w in range(len(topic_rel_data)):
            similarity_input[i_output-1][w] = topic_rel_data[w]

    print("similarity_input:", similarity_input.shape)

    return {'doc': similarity_input}, labels


def _kernel_layer(mu: float, sigma: float) -> keras.layers.Layer:
    """
    Gaussian kernel layer in KNRM.

    :param mu: Float, mean of the kernel.
    :param sigma: Float, sigma of the kernel.
    :return: `keras.layers.Layer`.
    """

    def kernel(x):
        return tf.math.exp(-0.5 * (x - mu) * (x - mu) / sigma / sigma)

    return keras.layers.Activation(kernel)


def build_keras_model():
    kernel_size = 5
    doc = Input(name='doc', shape=(3, 20))
    # print('doc shape : ', doc.shape)
    # print('doc : ', doc)
    KM = []
    for i in range(1, kernel_size): # no of kernels
        mu = 1. / (kernel_size - 1) + 2. / (kernel_size - 1) - 1.0 # 11 = max no. of kernels (hardcoded for dummy one
        sigma = 0.1
        if mu > 1.0:
            sigma = 0.001
            mu = 1.0
        mm_exp = _kernel_layer(mu, sigma)(doc)
        mm_doc_sum = keras.layers.Lambda(
            lambda x: tf.reduce_sum(x, 2))(mm_exp)
        mm_log = keras.layers.Activation(tf.math.log1p)(mm_doc_sum)
        mm_sum = keras.layers.Lambda(
            lambda x: tf.reduce_sum(x, 1))(mm_log)
        KM.append(mm_sum)

    phi = keras.layers.Lambda(lambda x: tf.stack(x, 1))(KM)
    out = keras.layers.Dense(1, activation='linear')(phi)
    model = keras.Model(inputs=[doc], outputs=[out])

    return model

model = build_keras_model()
model.summary()
model.compile(loss=rank_hinge_loss, optimizer='adam')  # adam

train_input, train_labels = get_train_input('/home/suchana/PycharmProjects/causalIR/neural-ranking-drmm/knrm/data/1.txt')

model.fit(train_input, train_labels, batch_size=10, verbose=2, shuffle=False, epochs=100)  # , callbacks=[c1])
model.save_weights('/home/suchana/PycharmProjects/causalIR/neural-ranking-drmm/knrm/data/foo.weights')
predictions = model.predict(train_input, batch_size=10)  # just to test, will rerank LM-scored docs
print('predict ::: ', predictions)
print('predict shape ::: ', predictions.shape)

# i = 0
# for topic, doc in pre_rank_data:
#     outFile.write(topic + '\t' + 'Q0' + '\t' + doc + "\t" + str(predictions[i][0]) + '\t' + 'drmmm' + '\n')
#     i += 1



