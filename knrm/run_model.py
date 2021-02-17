import sys
from keras.callbacks import ModelCheckpoint
from keras.utils import plot_model
from keras_model import build_keras_model
from load_data import *
from loss_function import *
import numpy as np
import os

# make sure the argument is good (0 = the python file, 1+ the actual argument)

if len(sys.argv) < 6:
    print('Needs 5 arguments - 1. run name, 2. train pair file (fold), 3. train similarity matrix file, '
          '4. test file (fold), 5. test similarity matrix file')
    exit(0)

run_name = sys.argv[1]
train_file = sys.argv[2]
train_file_cosim = sys.argv[3]
test_file = sys.argv[4]
test_file_cosim = sys.argv[5]

#
# build and train model
#
model = build_keras_model()
# model.summary()
model.compile(loss=rank_hinge_loss, optimizer='adam')  # adam
# plot_model(model, to_file='model.png', show_shapes=True)
train_input, train_labels = get_keras_train_input(train_file, train_file_cosim)
if not os.path.exists('/home/suchana/PycharmProjects/causalIR/neural-ranking-drmm/knrm/knrm_model_weights/'):
    os.makedirs('/home/suchana/PycharmProjects/causalIR/neural-ranking-drmm/knrm/knrm_model_weights/')
model.fit(train_input, train_labels, batch_size=10, verbose=2, shuffle=False, epochs=100)
model.save_weights('/home/suchana/PycharmProjects/causalIR/neural-ranking-drmm/knrm/knrm_model_weights/' + run_name + '.weights')

#
# prediction
#
# test_data, pre_rank_data = get_keras_test_input(test_file, test_file_cosim)
# predictions = model.predict(test_data, batch_size=10)
# if not os.path.exists('/home/suchana/PycharmProjects/causalIR/MatchZoo/knrm_model_weights/results/'):
#     os.makedirs('/home/suchana/PycharmProjects/causalIR/MatchZoo/knrm_model_weights/results/')
# with open('/home/suchana/PycharmProjects/causalIR/MatchZoo/knrm_model_weights/results/' + run_name + ".result", 'w') as outFile:
#     print("========== res file name : ", run_name, '===========')
#     i = 0
#     for topic, doc in pre_rank_data:
#         outFile.write(topic + '\t' + 'Q0' + '\t' + doc + '\t' + str(predictions[i][0]) + '\t' + 'knrm' + '\n')
#         i += 1
