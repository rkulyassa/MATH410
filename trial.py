import sys
import time
from simulated_annealing import SimulatedAnnealing

preference_map = {
    0: -1000,
    1: 0,
    2: 5,
    3: 10,
    4: 30,
    5: 100
}

sa = SimulatedAnnealing(
    csv_file=sys.argv[1],
    preference_map=preference_map,
    min_iterations=100000,
    stopping_iterations=10000,
    # min_iterations=194000,
    # stopping_iterations=194000,
    # min_iterations=279000,
    # stopping_iterations=279000,
    # min_iterations=322000,
    # stopping_iterations=322000,
    # initial_p=0.7
    # penalty_weight=10000
)

if __name__ == "__main__":
    start_time = time.perf_counter()

    sa.solve(persist_output_every=1000)
    sa.print_stats()
    # sa.output_csv_for_ha("./data/test.csv")

    end_time = time.perf_counter()
    print(f"Execution time: {end_time - start_time} seconds")