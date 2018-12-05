from spacy.matcher import PhraseMatcher
import spacy
nlp = spacy.load('en')

s = input("Enter String: ")

doc = nlp(s)


#words = [token.text for token in doc if token.is_stop != True and token.is_punct != True and token.pos_ == 'NOUN']
words = [token.text for token in doc if token.is_stop != True and token.is_punct != True and token.pos_ != 'NOUN']

print(words)
"""
apple_id = nlp.vocab.strings['apple']
print(str(nlp.vocab[apple_id]))
def on_match(matcher, doc, id, matches):
    print('Matched!', matches)

matcher = PhraseMatcher(nlp.vocab)
matcher.add('OBAMA', on_match, nlp(u"Barack Obama"))
matcher.add('HEALTH', on_match, nlp(u"health care reform"),
                                nlp(u"healthcare reform"))
doc = nlp(u"Barack Obama urges Congress to find courage to defend his healthcare reforms")
matches = matcher(doc)
print(matches)

"""

"""
matcher = PhraseMatcher(nlp.vocab)
matcher.add('OBAMA', None, nlp(u"Barack Obama"))
doc = nlp(u"Barack Obama lifts America one last time in emotional farewell")
matches = matcher(doc)
print(matches)
"""