import csv

from hungarian_algorithm import algorithm

if __name__ == "__main__":
    with open("data/FA22.csv") as f:
        reader = csv.reader(f)
        rows = list(reader)
    
    G = {}

    class_names = rows[0][1:]

    for row in rows[1:]:
        timestamp = row[0]
        G[timestamp] = {}
        for i, v in enumerate(row[1:]):
            if v.strip():
                preference = int(v.strip())
                if preference:
                    G[timestamp][class_names[i]] = int(preference)
    
    # print(G)


    optimal_matching = algorithm.find_matching(
        G, matching_type="max", return_type="list"
    )
    print(optimal_matching)
    score = sum([g[1] for g in optimal_matching])
    print(score)
