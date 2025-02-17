from annealing.annealing import calculate_spread
from annealing.typing import *

a = Course("a", 5)
b = Course("b", 8)
c = (Course("c", 6),)

matching = [
    Match(None, a),
    Match(None, a),
    Match(None, b),
    Match(None, b),
    Match(None, b),
    Match(None, c),
    Match(None, c),
    Match(None, c),
    Match(None, c),
    Match(None, c),
]

variance = calculate_spread(matching)
print("Variance:", variance)
