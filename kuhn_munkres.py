import csv
import time
import sys
from munkres import Munkres, print_matrix, DISALLOWED

if __name__ == "__main__":
    start_time = time.perf_counter()

    with open(sys.argv[1]) as f:
        reader = csv.reader(f)
        rows = list(reader)
    
    # construct adjacency matrix
    matrix = []
    preference_rows = [row[1:] for row in rows[2:]]
    for row in preference_rows:
        r = []
        for entry in row:
            if entry.strip():
                v = int(entry.strip())
                r.append(v)
            else:
                r.append(DISALLOWED) # analagous to infinity
        matrix.append(r)


    # duplicate columns until the matrix is square
    capacities = [int(v) for v in rows[1][1:]]
    print("Capacities:", capacities)
    for i, c in enumerate(capacities):
        for _ in range(c - 1):
            for row in matrix:
                row.append(row[i])
    
    print("Rows (students):", len(matrix))
    print("Columns (seats):", len(matrix[0]))


    # from https://software.clapper.org/munkres/
    m = Munkres()
    matrix2 = matrix.copy()
    indexes = m.compute(matrix2)
    # print_matrix(matrix, msg='Lowest cost through this matrix:')
    total = 0
    for row, column in indexes:
        value = matrix[row][column]
        total += value
        print(f'({row}, {column}) -> {value}')
    print(f'total cost: {total}')

    end_time = time.perf_counter()
    print(f"Execution time: {end_time - start_time} seconds")