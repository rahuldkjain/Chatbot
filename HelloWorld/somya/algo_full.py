from nltk.tokenize import word_tokenize
import nltk
from nltk.corpus import stopwords
import csv
import spacy
from collections import Counter

MIN_MATCH_SCORE = 0.85
stop_words = set(stopwords.words('english'))

def jaro(s, t):
    s_len = len(s)
    t_len = len(t)

    if s_len == 0 and t_len == 0:
        return 1

    match_distance = (max(s_len, t_len) // 2) - 1

    s_matches = [False] * s_len
    t_matches = [False] * t_len

    matches = 0
    transpositions = 0

    for i in range(s_len):
        start = max(0, i-match_distance)
        end = min(i+match_distance+1, t_len)

        for j in range(start, end):
            if t_matches[j]:
                continue
            if s[i] != t[j]:
                continue
            s_matches[i] = True
            t_matches[j] = True
            matches += 1
            break

    if matches == 0:
        return 0

    k = 0
    for i in range(s_len):
        if not s_matches[i]:
            continue
        while not t_matches[k]:
            k += 1
        if s[i] != t[k]:
            transpositions += 1
        k += 1

    return ((matches / s_len) +
            (matches / t_len) +
            ((matches - transpositions/2) / matches)) / 3

def getFreq(file):
    fields = {}
    with open(file, 'r') as csvfile:
        # creating a csv reader object
        csvreader = csv.reader(csvfile)
        # extracting each data row one by one
        for row in csvreader:
            row = row[4:len(row)]
            for word in row:
                if word in fields.keys():
                    fields[word] += 1
                else:
                    fields[word] = 1
    return fields

def getField(file):
    fields = []
    with open(file, 'r') as csvfile:
        # creating a csv reader object
        csvreader = csv.reader(csvfile)
        # extracting each data row one by one
        for row in csvreader:
            row.pop(list(row).index(''))
            fields.append(row)
    return fields


def getSynonyms(file):
    syn = {}
    with open(file, 'r') as csvfile:
        # creating a csv reader object
        csvreader = csv.reader(csvfile)

        # extracting each data row one by one
        for row in csvreader:
            if row is not None:
                syn[row[0]] = [row[0]]
                for i in range(1, len(row)):
                    if row[i] == '':
                        break
                    syn[row[0]].append(row[i])

    return syn


def phrase_match(fields,syn,query) :
    scores = []
    for f in range(0,len(fields)) :
        new_query = []
        score = 0
        field = fields[f]
        #checking singly
        for ele in query:
            w = ele.lower()
            for l in field :
                ja = jaro(w.lower(),l.lower())
                if ja>=MIN_MATCH_SCORE :
                    score += ja
                    new_query.append(l)
                else :
                    if l in syn.keys():
                        for s in syn[l] :
                            ja = jaro(w.lower(),s.lower())
                            if ja >= MIN_MATCH_SCORE:
                                score += ja
                                new_query.append(l)
        #checking doubly
        for i in range(0,len(new_query)-1):
            for j in range(0,len(field)-1) :
                if new_query[i] == field[j] and new_query[i+1] == field[j+1] :
                    score += 1
        #checking tripplets
        for i in range(0,len(new_query)-2):
            for j in range(0,len(field)-2) :
                if new_query[i] == field[j] and new_query[i+1] == field[j+1]  and new_query[i+2] == field[j+2]:
                    score += 1
        scores.append(score)
    return scores

def phrase_match_with_wordBag(fields,syn,query,freq,wsyn):
    matchScores = []
    lengthScores = []
    qlen = len(query)
    for f in range(0,len(fields)) :
        new_query = []
        score = 0

        field = fields[f]
        field = field[4:len(field)]

        #calculating match score

        #checking singly
        for ele in query:
            w = ele.lower()
            for l in field :
                ja = jaro(w.lower(),l.lower())
                if ja >= MIN_MATCH_SCORE :
                    score += ja/freq[l]
                    new_query.append(l)
                    #field.pop(field.index(l))  # 1 word = 1 match
                else :
                    if l in syn.keys():
                        for s in syn[l] :
                            ja = jaro(w.lower(),s.lower())
                            if ja >= MIN_MATCH_SCORE:
                                score += (wsyn*ja)/freq[l]
                                new_query.append(l)
                                #field.pop(field.index(l))  # 1 word = 1 match
                                #break
                #print(field)
            #print()
        #checking doubly
        for i in range(0,len(new_query)-1):
            for j in range(0,len(field)-1) :
                if new_query[i] == field[j] and new_query[i+1] == field[j+1] :
                    score += 1
        #checking tripplets
        for i in range(0,len(new_query)-2):
            for j in range(0,len(field)-2) :
                if new_query[i] == field[j] and new_query[i+1] == field[j+1]  and new_query[i+2] == field[j+2]:
                    score += 1
        matchScores.append(score)

        # calculating length score
        lengthScores.append(abs(1 - qlen / len(field)))

    #performing length weighting tiebreaker

    m = max(matchScores)
    minLengthScoreIndex = matchScores.index(m)
    minLengthScore = lengthScores[minLengthScoreIndex]
    if(matchScores.count(m)>1):
        for i in range(0,len(matchScores)):
            if matchScores[i] == m :
                if lengthScores[i] <= minLengthScore:
                    minLengthScore = lengthScores[i]
                    minLengthScoreIndex = i

    return fields[minLengthScoreIndex][2]

def query_grouping_with_stop_removal(sentence):
    big_groupings = []
    i = 0
    k = 0
    sentiment = []
    tagged = nltk.pos_tag(word_tokenize(sentence))
    while k < (len(tagged)):
        groupings = []
        i = k
        senti = []
        if tagged[i][1] == 'RB' or tagged[i][1] == 'RP' or tagged[i][1] == 'NNS' or tagged[i][1] == 'NNP' or tagged[i][1] == 'NN' or tagged[i][1] == 'JJ' or tagged[i][1] == 'VBG' or tagged[i][1] == 'VBZ' or tagged[i][1] == 'VBP' or tagged[i][1] == 'VBN' or tagged[i][1] == 'DT'  or tagged[i][1] == 'VBD':
            while tagged[i][1] == 'RB' or tagged[i][1] == 'IN' or tagged[i][1] == 'RP' or tagged[i][1] == 'NNS' or tagged[i][1] == 'NNP' or tagged[i][1] == 'NN' or tagged[i][1] == 'JJ' or tagged[i][1] == 'VBG' or tagged[i][1] == 'WRB' or tagged[i][1] == 'WP' or tagged[i][1] == 'VBZ' or tagged[i][1] == 'VBP' or tagged[i][1] == 'VBN'  or tagged[i][1] == 'DT'  or tagged[i][1] == 'VBD':

                groupings.append(tagged[i][0])
                senti.append(word_tokenize(sentence)[i])
                #senti = ''.join(senti)
                i = i + 1
                k = i
                if i == len(tagged):
                    break
            big_groupings.append(groupings)
            sentiment.append(''.join(senti))
        else:
            sentiment.append(word_tokenize(sentence)[k])
            k = k + 1
    final_groups = []
    for group in big_groupings:
        gr = []
        for w in group:
            if w not in stop_words:
                gr.append(w)
        final_groups.append(gr)
    return final_groups

#main code starts here

print("Loading data ...")
fields = getField('fieldToken2.csv')
syn = getSynonyms('withSynUpd3.csv')
freq = getFreq('fieldToken2.csv')

#print(freq)
print("processing queries ...")
Syn_weight = 0.9

test = ["what is the number of children in"
,"show me the number of male iliterates in"
,"how many full time farmers are in"
,"how many females are part time working in household industry"
,"how many schools are in",
"how many villages in are not electrified?",
"share of houses with health insurance in",
"percentage women using condom as contraceptive",
"how many women are availing prenatal services",
"what percentage of children received all vaccination",
"what percentage of children are anemic in",
"how many males in are sufferring though high level of blood sugar",
"how many households above poverty line does not have a toilet",
"how many scheduled tribe households were issueda job card",
"how many people were employed under mgnrega scheme",
"what is the education situation"]

t = ["what is the education situation"]

for q in test:
    print(q)
    queries = query_grouping_with_stop_removal(q)
    for query in queries:
        result = phrase_match_with_wordBag(fields, syn, query, freq,Syn_weight)
        #print(query)
        print(result)
        print()
    print("---------------------------------------------------------------")










