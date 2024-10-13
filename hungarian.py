from hungarian_algorithm import algorithm
from data import SH

if __name__ == "__main__":
    optimal_matching = algorithm.find_matching(
        SH, matching_type="max", return_type="list"
    )
    print(optimal_matching)
    score = sum([g[1] for g in optimal_matching])
    print(score)
