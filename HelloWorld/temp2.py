from glove import Glove
from glove import Corpus


# reads .txt files
def read_corpus(filename):

    delchars = [chr(c) for c in range(256)]
    delchars = [x for x in delchars if not x.isalnum()]
    delchars.remove(' ')
    delchars = ''.join(delchars)
    table = str.maketrans(dict.fromkeys(delchars))

    with open(filename, 'r') as datafile:
        for line in datafile:
            yield line.lower().translate(table).split(' ')


get_data = read_corpus('data/articles.txt')
corpus_model = Corpus()
corpus_model.fit(get_data, window=10)
epochs = 1000
no_threads = 8
glove = Glove(no_components=100, learning_rate=0.05)
glove.fit(corpus_model.matrix, epochs=epochs, no_threads=no_threads, verbose=True)
glove.add_dictionary(corpus_model.dictionary)

print("Most similar to Male ==>" + str(glove.most_similar('male')))
print("---------------------------------------------------------------------------")
print("Most similar to Population ==>" + str(glove.most_similar('population')))
print("---------------------------------------------------------------------------")
print("Most similar to Workers ==>" + str(glove.most_similar('workers')))
print("---------------------------------------------------------------------------")
print("Most similar to Main ==>" + str(glove.most_similar('main')))
print("---------------------------------------------------------------------------")
print("Most similar to Marginal ==>" + str(glove.most_similar('marginal')))
print("---------------------------------------------------------------------------")
print("Most similar to Agricultural ==>" + str(glove.most_similar('agricultural')))
print("---------------------------------------------------------------------------")
print("Most similar to Condom ==>" + str(glove.most_similar('condom')))
print("---------------------------------------------------------------------------")
print("Most similar to Children ==>" + str(glove.most_similar('children')))
print("---------------------------------------------------------------------------")

"""
glove = Glove()
glove = glove.load('models/wiki-meta_glove.model')
print(glove.most_similar('male'))


glove = Glove()
stanford = glove.load_stanford('data/glove.68/glove.68.200d.txt')

x = stanford.word_vectors[stanford.dictionary['woman']][:10]
y = stanford.most_similar('woman')

print('vectors of woman')
print(x)
print(-----------------)
print('Most similar to woman')
print(y)
"""