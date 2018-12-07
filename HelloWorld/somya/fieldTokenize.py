import csv
import spacy
nlp = spacy.load('en')

FIELDFILE = "schema.csv"
SYNFILE = "/home/swaniti8/withSyn.csv"
FIELDTOKEN = "fieldToken2.csv"

def fieldTokenize():
    fields = []
    with open(FIELDFILE, 'r') as csvfile:
        # creating a csv reader object
        csvreader = csv.reader(csvfile)

        # extracting each data row one by one
        for row in csvreader:
            metric = str(row[2])
            metric = metric.replace("("," ")
            metric = metric.replace(")"," ")
            metric = metric.replace("+", " ")
            metric = metric.replace("-", " ")
            metric = metric.replace("/", " ")
            metric = metric.replace("APL", "Above poverty line")
            metric = metric.replace("BPL", "Below poverty line")
            metric = metric.replace("SC", "scheduled caste")
            metric = metric.replace("ST", "scheduled tribes")
            metric = metric.replace("HH", "Households")
            metric = metric.replace("No", "number")
            print(metric)
            doc = nlp(metric)

            outputRow = row[0:4]
            tokens = [token.text for token in doc if token.is_stop != True and token.is_punct != True ]
            for token in tokens:
                if token != '  ' and token != '   ':
                    outputRow.append(token.lower())
            fields.append(outputRow)
    with open(FIELDTOKEN, "w") as f:
        for values in fields:
            st = ''
            for ele in values:
                st += ele + ','
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

fieldTokenize()
#print(synonyms())