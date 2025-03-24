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
        3: 50,
        4: 100,
        5: 1000
    }
    sa = SimulatedAnnealing(
        csv_file="./data/FA22.csv",
        preference_map=preference_map,
        # initial_temperature=1000,
        # cooling_rate=0.995
        initial_temperature=1e20,
        cooling_rate=0.9995
    )
    sa.solve()
    sa.print_matching()
    sa.print_stats()

if __name__ == "__main__":
    # trial_1()
    trial_2()