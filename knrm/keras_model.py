import keras
from keras.models import Sequential, Model
from keras.layers import Input, Embedding, Dense, Activation, Add, Lambda, Permute, Dropout, Flatten
from keras.layers import Reshape, Dot
from keras.activations import softmax
from keras.layers import Conv2D, MaxPooling2D
import numpy as np
import tensorflow as tf


query_term_maxlen = 5
doc_maxlen = 100
kernel_size = 5


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

#
# returns the raw keras model object
#
def build_keras_model():
    doc = Input(name='doc', shape=(query_term_maxlen, doc_maxlen))
    # print('doc shape : ', doc.shape)
    # print('doc : ', doc)
    KM = []
    for i in range(2, kernel_size): # no of kernels
        mu = 1. / (i - 1) + 2. / (i - 1) - 1.0
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

