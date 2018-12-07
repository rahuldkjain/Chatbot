# importing csv module
import csv
from thesaurus import Word


# csv file name
filename = "fieldToken2.csv"
newfile = "withSynUpd3.csv"

# initializing the titles and rows list
fields = []
words = {}

# reading csv file
with open(filename, 'r') as csvfile:
    # creating a csv reader object
    csvreader = csv.reader(csvfile)

    # extracting field names through first row

    # extracting each data row one by one
    for row in csvreader:
        row = row[4:len(row)]
        for ele in row:
            for x in ele.split():
                if x not in words.keys():
                    words[x] = [x]
                    w = Word(x)
                    syno = w.synonyms()
                    print(syno)
                    if syno is not None:
                        for s in syno:
                            words[x].append(s)


print(words)

with open(newfile, "w") as f:
    for values in words.values():
        st = ''
        if len(values) < 8:
            for ele in values:
                st += ele + ','
        else:
            for ele in values[0:9]:
                st += ele + ','

        print(st)
        print(st, file=f)