import csv
from simulated_annealing import SimulatedAnnealing

def trial_1():
    preference_map = {
        0: -1000,
        1: 0,
        2: 10,
        3: 20
    }

    # sa.solve(log_verbose=True)
    results = []
    for _ in range(100):
        sa = SimulatedAnnealing(
            csv_file="./data/trivial.csv",
            preference_map=preference_map,
            initial_temperature=100,
            cooling_rate=0.995
        )
        sa.solve()
        results.append(sa.eval_score(sa.current_matching))
        # sa.print_matching()
        # print(sa.temperature)

    # print(results)
    print(sum(results) / len(results))

def trial_2():
    preference_map = {
        0: -1000,
        1: -50,
        2: 0,
        3: 25,
        4: 75,
        5: 100
    }
    sa = SimulatedAnnealing(
        csv_file="./data/FA22.csv",
        preference_map=preference_map,
    )

    print(sa.temperature)
    print(sa.cooling_rate)
    # sa.solve()
    # sa.print_matching()
    # sa.print_stats()
    # sa.output_csv_for_ha("./data/test.csv")

if __name__ == "__main__":
    # trial_1()
    trial_2()

    # with open("data/FA22.csv") as f:
    #     reader = csv.reader(f)
    #     rows = list(reader)
    
    # sums = []
    # for i in range(len(rows[0][1:])):
    #     nums = []
    #     for row in rows[2:]:
    #         nums.append(int(row[i+1]))
    #     sums.append(sum(nums))
    
    # total = sum(sums)
    # result = [round(s/total*322) for s in sums]
    # print(result)
    # print(sum(result))
    # # [15, 31, 15, 21, 17, 12, 8, 10, 10, 4, 24, 9, 14, 11, 21, 7, 11, 25, 12, 12, 18, 16]