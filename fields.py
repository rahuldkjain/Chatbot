import csv
import spacy
nlp = spacy.load('en')

source = "/home/swaniti8/source.csv"
FIELDFILE = "/home/swaniti8/fields.csv"
SYNFILE = "/home/swaniti8/withSyn.csv"
FIELDTOKEN = "/home/swaniti8/fieldToken.csv"

def field():
    fields = []
    with open(FIELDFILE, 'r') as csvfile:
        # creating a csv reader object
        csvreader = csv.reader(csvfile)

        # extracting each data row one by one
        for row in csvreader:
            doc = nlp(str(row))
            fields.append([token.text for token in doc if token.is_stop != True and token.is_punct != True])
    with open(FIELDTOKEN, "w") as f:
        for values in fields:
            st = ''
            for ele in values:
                st += ele + ','
            print(st)
            print(st, file=f)
    return fields

def synonyms():
    syn = {}
    with open(SYNFILE, 'r') as csvfile:
        # creating a csv reader object
        csvreader = csv.reader(csvfile)

        # extracting each data row one by one
        for row in csvreader:
            syn[row[0]] = [row[0]]
            for i in range(1,len(row)):
                if row[i] == '':
                    break
                syn[row[0]].append(row[i])

    return syn

print(field())
print(synonyms())

