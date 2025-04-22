import csv
import sys

preference_map = {
    0: -1000,
    1: 0,
    2: 5,
    3: 10,
    4: 30,
    5: 100
}

with open(sys.argv[1]) as f:
    reader = csv.reader(f)
    data = list(reader)

for i, row in enumerate(data[2:]):
    for j, entry in  enumerate(row[1:]):
        data[i+2][j+1] = preference_map[int(entry)]

with open(sys.argv[2], 'w') as f:
    writer = csv.writer(f)
    writer.writerows(data)