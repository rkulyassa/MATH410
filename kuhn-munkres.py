import csv
from munkres import Munkres, print_matrix, DISALLOWED

if __name__ == "__main__":
    with open("data/FA22.csv") as f:
        reader = csv.reader(f)
        rows = list(reader)
    
    # construct adjacency matrix
    matrix = []
    rows = [row[1:] for row in rows[1:]]
    for row in rows:
        r = []
        for entry in row:
            if entry.strip():
                v = int(entry.strip())
                r.append(-v + 5) # invert preferences to make it a minimization problem
            else:
                r.append(DISALLOWED) # analagous to infinity
        matrix.append(r)


    # duplicate columns until the matrix is square
    i = 0
    while len(matrix) > len(matrix[0]):
        for row in matrix:
            row.append(row[i])
        i += 1
        if i == 22:
            i = 0
    
    # for m in matrix:
    #     print(m)
    # print(len(matrix))
    # print(len(matrix[0]))


    # from https://software.clapper.org/munkres/
    m = Munkres()
    indexes = m.compute(matrix)
    print_matrix(matrix, msg='Lowest cost through this matrix:')
    total = 0
    for row, column in indexes:
        value = matrix[row][column]
        total += value
        print(f'({row}, {column}) -> {value}')
    print(f'total cost: {total}')