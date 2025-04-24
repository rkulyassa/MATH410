import csv
import sys

with open(sys.argv[1]) as f:
    reader = csv.reader(f)
    rows = list(reader)

for i, row in enumerate(rows[2:]):
    preferences = [int(e) for e in row[1:]]
    s = sum(preferences)
    if s != 15:
        print(row[0], s, "!!!")
    else:
        print(row[0], s)