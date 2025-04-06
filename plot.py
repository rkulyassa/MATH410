import matplotlib.pyplot as plt
import re

with open("trial.txt") as f:
    lines = f.readlines()

data = []

for line in lines:
    if line.startswith("I:"):
        data.append(list(map(float, re.findall(r'[-+]?\d*\.\d+e[+-]?\d+|[-+]?\d+', line))))

plt.plot([d[0] for d in data], [d[2] for d in data])

plt.xlabel("Iteration")
plt.ylabel("Score")
plt.title("T=100, CR=0.99")

plt.show()
