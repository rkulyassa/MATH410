import csv
import sys
from uuid import uuid4

with open(sys.argv[1]) as f:
    reader = csv.reader(f)
    data = list(reader)

x = len(data[0])
y = len(data)

# duplicate course titles
for i in range(x-1):
    data[0].append(data[0][i+1])

# duplicate rows
for i in range(y-2):
    data.append(data[i+2].copy())

# duplicate columns
for j in range(x-1):
    for i in range(len(data)-1):
        data[i+1].append(data[i+1][j+1])

# set all courses and student ids to uuid4s to ensure uniqueness
for row in data[1:]:
    row[0] = uuid4()
for i, e in enumerate(data[0][1:]):
    data[0][i+1] = uuid4()

with open(sys.argv[2], 'w') as f:
    writer = csv.writer(f)
    writer.writerows(data)