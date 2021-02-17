import logging
import multiprocessing
import os
import sys
from gensim.models.word2vec import LineSentence
from gensim.models.word2vec import Word2Vec


if __name__ == '__main__':
    program = os.path.basename(sys.argv[0])
    logger = logging.getLogger(program)

    logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s')
    logging.root.setLevel(level=logging.INFO)
    logger.info("Running %s", ' '.join(sys.argv))

    # Check and process input arguments.
    if len(sys.argv) < 4:
        print(globals()['__doc__'] % locals())
        sys.exit(1)

    inp, outp, veco = sys.argv[1:4]

    max_length = 0
    with open(inp, 'r') as f:
        for line in f.readlines():
            max_length = max(max_length, len(line))
    logger.info("Max article length: %s words.", max_length)

    params = {
        'size': 100,
        'window': 5,
        'min_count': 1,  # will not generate vector if the term does not occur at least 10 times
        'workers': max(1, multiprocessing.cpu_count() - 1),
        'sample': 1E-5,
        'sg': 1,
    }
    word2vec = Word2Vec(LineSentence(inp, max_sentence_length=max_length), **params)
    word2vec.save(outp)

    if veco:
        word2vec.wv.save_word2vec_format(outp + '.model.txt', binary=False)
