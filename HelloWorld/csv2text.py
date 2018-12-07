import csv


newfile = "/home/swaniti6/PycharmProjects/HelloWorld/fields.csv"

"""
with open(newfile, "w") as f:
    for values in words.values():
        st = ''
        for ele in values:
            st += ele + ','

        print(st)
        print(st, file=f)
"""
with open(newfile, 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    print(34)
    print(list(csvreader))
    for row in csvreader:
        print(row)

