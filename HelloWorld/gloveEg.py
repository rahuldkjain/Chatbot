import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from glove import Corpus, Glove

#nltk.download()

#list of sentences to be vectorized

lines = ['Hello this is a tutorial on how to convert the word in an integer format', 'this is a beautiful day',
         'Jack is going to office']

stop_words = set(stopwords.words('english'))
lines_without_stopwords = []

#stop words contain the set of stop words
for line in lines:
    temp_line = []
    for word in lines:
        if word not in stop_words:
            temp_line.append(word)
            string=' '
            lines_without_stopwords.append(string.join(temp_line))
            lines=lines_without_stopwords


wordnet_lemmatizer = WordNetLemmatizer()
lines_with_lemmas = []

#stop words contain the set of stop words

for line in lines:
    temp_line = []
    for word in lines:
        temp_line.append(wordnet_lemmatizer.lemmatize(word))
    string = ' '
    lines_with_lemmas.append(string.join(temp_line))

lines = lines_with_lemmas

# creating a corpus object
corpus = Corpus()
# training the corpus to generate the co occurence matrix which is used in GloVe
corpus.fit(lines, window=10)
# creating a Glove object which will use the matrix created in the above lines to create embeddings
# We can set the learning rate as it uses Gradient Descent and number of components
glove = Glove(no_components=5, learning_rate=0.05)

glove.fit(corpus.matrix, epochs=30, no_threads=4, verbose=True)
glove.add_dictionary(corpus.dictionary)
glove.save('glove.model')




