import csv
import sys
from math import ceil

with open(sys.argv[1]) as f:
    reader = csv.reader(f)
    rows = list(reader)

sums = []
for i in range(len(rows[0][1:])):
    nums = []
    for row in rows[2:]:
        nums.append(int(row[i+1]))
    sums.append(sum(nums))

total = sum(sums)
result = [ceil(s/total*(len(rows)-2)) for s in sums]
print(result)
print(sum(result))