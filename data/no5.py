import csv
import sys

with open(sys.argv[1]) as f:
    reader = csv.reader(f)
    rows = list(reader)

counts = []
for i in range(len(rows[0][1:])):
    count=0
    for row in rows[2:]:
        if row[i+1] == "5":
            count += 1
    counts.append(count)

print(counts)
print(sum(counts))