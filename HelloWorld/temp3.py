# importing csv module
import csv
"""
import requests
from bs4 import BeautifulSoup

class SynAntDictionary(object):
    @staticmethod
    def synonym(Word):

        if len(Word.split()) > 1:
            print("Error: A Term must be only a single word")
        else:
            try:
                data = requests.get("http://www.thesaurus.com/browse/" + Word)
                Selection = BeautifulSoup(data.text, "lxml")
                Synterms = Selection.find(class_="postab-container css-1nq2eka e9i53te1").find_all("strong")
                "Filter and format Syn Terms into Comma Delineated String"
                t = 0


                while t < len(Synterms):
                    if t == 0:
                        SynList = Synterms[t]
                    else:

                        SynList = str(SynList) + "," + str(Synterms[t])
                    t = t + 1
                SynList = SynList.replace("<strong>", "")
                SynList = SynList.replace("</strong>", "")
                SynList = SynList.replace(", ", ",")


                return SynList.split(',')
            except:
                print(str(Word) + " has no Synonyms in the API")

syn = SynAntDictionary()
"""
# csv file name
filename = "/home/swaniti6/PycharmProjects/HelloWorld/fields.csv"
newfile = "/home/swaniti6/PycharmProjects/HelloWorld/articles.txt"

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
        x = str(row)
        x = x.replace("['", "")
        x = x.replace('["', '')
        x = x.replace('"]', '')
        x = x.replace("']", "")
        x = x.replace("(", "")
        x = x.replace(")", "")
        x = x.replace("  ", "")
        x = x.lower()
        fields.append(x)


with open(newfile, "w") as f:
    for values in fields:
        print(values, file=f)

