import csv
import gensim
import logging
import os
#import spacy
#nlp = spacy.load('en')

logging.basicConfig(
    format='%(asctime)s : %(levelname)s : %(message)s',
    level=logging.INFO)


def show_file_contents(input_file):
    with open(input_file, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        for line in csvreader:
            print(line)
            break


def read_input(input_file):
    """This method reads the input file which is in csv format"""

    logging.info("reading file {0}...this may take a while".format(input_file))
    with open(input_file, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        for i, line in enumerate(csvreader):

            if i % 10000 == 0:
                logging.info("read {0} reviews".format(i))
            # do some pre-processing and return list of words for each review
            # text
            x = ''
            for ele in line:
                x += str(ele).lower() +' '
            print(x)
            yield gensim.utils.simple_preprocess(str(x))


if __name__ == '__main__':

    abspath = os.path.dirname(os.path.abspath(__file__))
    data_file = os.path.join(abspath, "./fieldToken.csv")

    # read the tokenized reviews into a list
    # each review item becomes a serries of words
    # so this becomes a list of lists
    documents = list(read_input(data_file))
    logging.info("Done reading data file")

    # build vocabulary and train model
    model = gensim.models.Word2Vec(
        documents,
        size=20,
        window=4,
        min_count=2,
        workers=10)
    for i in range(200):
        model.train(documents, total_examples=len(documents), epochs=10)

    # save only the word vectors
    model.wv.save(os.path.join(abspath, "../ret.csv"))

    w1 = "population"
    print("Most similar to {0}".format(w1), model.wv.most_similar(positive=w1))

    w1 = "mother"
    print("Most similar to {0}".format(w1), model.wv.most_similar(positive=w1))

    # look up top 6 words similar to 'polite'
    w1 = "household"
    print(
        "Most similar to {0}".format(w1),
        model.wv.most_similar(
            positive=w1,
            topn=6))

    # look up top 6 words similar to 'france'
    w1 = "agricultural"
    print(
        "Most similar to {0}".format(w1),
        model.wv.most_similar(
            positive=w1,
            topn=6))

    # look up top 6 words similar to 'shocked'
    w1 = "children"
    print(
        "Most similar to {0}".format(w1),
        model.wv.most_similar(
            positive=w1,
            topn=6))

    # look up top 6 words similar to 'shocked'
    w1 = "workers"
    print(
        "Most similar to {0}".format(w1),
        model.wv.most_similar(
            positive=w1,
            topn=6))

    w1 = "total"
    print(
        "Most similar to {0}".format(w1),
        model.wv.most_similar(
            positive=w1,
            topn=6))

    # get everything related to stuff on the bed
    w1 = ["marginal", 'main', 'workers']
    w2 = ['industry']
    print(
        "Most similar to {0}".format(w1),
        model.wv.most_similar(
            positive=w1,
            negative=w2,
            topn=10))

    # similarity between two different words
    print("Similarity between 'sex' and 'ratio'",
          model.wv.similarity(w1="sex", w2="ratio"))

    # similarity between two identical words
    print("Similarity between 'household' and 'children'",
          model.wv.similarity(w1="household", w2="children"))

    # similarity between two unrelated words
    print("Similarity between 'main' and 'workers'",
          model.wv.similarity(w1="main", w2="workers"))

    print("Similarity between 'marginal' and 'workers'",
          model.wv.similarity(w1="marginal", w2="workers"))
