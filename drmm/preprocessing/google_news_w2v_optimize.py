from gensim.models.keyedvectors import KeyedVectors
from collections import defaultdict
from nltk.stem import PorterStemmer

# load .txt w2v file
model_txt = KeyedVectors.load_word2vec_format('/store/causalIR/drmm/data/GoogleNews-vectors-negative300.txt', binary=False)

# Get a list of words in the vocabulary
voca_list = model_txt.wv.vocab.keys()
# print(words)
stemmer = PorterStemmer()
# voca_list = ['baby', 'Babies', 'Apple', 'babylike', 'baby', 'Orange', 'oranges']

map_dict = defaultdict(list)
for term in voca_list:
    # print(term)
    curr = term
    # print(curr)
    ts = stemmer.stem(term.lower().strip())
    # print(ts)
    if ts in map_dict:
        # print('here')
        map_dict[ts].append(curr)
    else:
        # print('now here')
        map_dict[ts].append(curr)
print(map_dict)
print('\n', len(map_dict))

# Make a dictionary
# word_vec_dict = {word: model_txt.wv[word] for word in words}

# out = open('/store/causalIR/drmm/data/output.txt', 'w')
# for k, v in word_vec_dict.items():
#     out.write(str(k))
#     out.write(' ')
#     for i in v:
#         out.write(str(i))
#         out.write(' ')
#     out.write('\n')
#
# out.close()