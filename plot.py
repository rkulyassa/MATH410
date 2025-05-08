import matplotlib.pyplot as plt
import re
import sys

with open(sys.argv[1]) as f:
    lines = f.readlines()

data = []

for line in lines:
    if line.startswith("I:"):
        data.append(list(map(float, re.findall(r'[-+]?\d*\.\d+|[-+]?\d+', line))))

fig, ax1 = plt.subplots()

# ax1.plot([d[0] for d in data], [d[1] for d in data], 'g-', linewidth=0.5, label='Iterations since improvement')
# ax1.set_xlabel("Iteration")
# ax1.set_ylabel("Iterations since improvement", color='g')
# ax1.tick_params(axis='y', labelcolor='g')

ax1.plot([d[0] for d in data], [d[2] for d in data], linewidth=0.5, label='Score')
ax1.set_xlabel("Iteration")
ax1.set_ylabel("Score", color='b')
ax1.tick_params(axis='y', labelcolor='b')

ax2 = ax1.twinx()
ax2.plot([d[0] for d in data], [d[3] for d in data], 'r-', linewidth=0.5, label='Temperature')
ax2.set_ylabel("Temperature", color='r')
ax2.tick_params(axis='y', labelcolor='r')
ax2.set_zorder(2)

# ax3 = ax1.twinx()
# ax3.spines["right"].set_position(("axes", 1.1))  # 1.1 means 10% to the right of the original
# ax3.plot([d[0] for d in data], [d[1] for d in data], 'g-', linewidth=0.5, label='Iterations since improvement')
# ax3.set_ylabel("Iterations since improvement", color='g')
# ax3.tick_params(axis='y', labelcolor='g')
# ax3.set_zorder(1)


# plt.title("P_i = 0.7, P_f = 0.1")

fig.tight_layout()

plt.show()
