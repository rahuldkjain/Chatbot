import nltk
nltk.download('wordnet')
from nltk.corpus import wordnet

synonyms = []
antonyms = []

for syn in wordnet.synsets("males"):

    for l in syn.lemmas():
        for sim in l.similar_tos():
            print(' {}'.format(sim))
        synonyms.append(l.name())
        if l.antonyms():
            antonyms.append(l.antonyms()[0].name())

print(set(synonyms))
#print(set(antonyms))
