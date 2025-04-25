import csv
import time
import sys
from munkres import Munkres, print_matrix, DISALLOWED

if __name__ == "__main__":
    start_time = time.perf_counter()

    with open(sys.argv[1]) as f:
        reader = csv.reader(f)
        rows = list(reader)

    student_ids = [row[0] for row in rows[2:]]
    course_titles = rows[0][1:]

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
    
    for r in matrix:
        print(r)


    # duplicate columns until the matrix is square
    capacities = [int(v) for v in rows[1][1:]]
    print("Capacities:", capacities)
    offset = 0
    for i, c in enumerate(capacities):
        for _ in range(c - 1):
            for j, row in enumerate(matrix):
                matrix[j] = row[:i+offset] + [row[i+offset]] + row[i+offset:]
        offset += c-1
    for r in matrix:
        print(r)
    
    print("Rows (students):", len(matrix))
    print("Columns (seats):", len(matrix[0]))


    # from https://software.clapper.org/munkres/
    m = Munkres()
    matrix2 = matrix.copy()
    indexes = m.compute(matrix2)

    course_fulfillment = {course: 0 for course in course_titles}

    seat_to_course = []
    for i, cap in enumerate(capacities):
        seat_to_course.extend([i] * cap)

    for row, col in indexes:
        course_index = seat_to_course[col]
        course_title = course_titles[course_index]
        course_fulfillment[course_title] += 1

    for i, course in enumerate(course_titles):
        print(f"Course '{course}' filled {course_fulfillment[course]}/{capacities[i]}")

    preference_values = [-100, -30, -10, -5, 0, 1000]
    choice_counts = {v: 0 for v in range(5)}
    total_choice_index = 0
    for row, col in indexes:
        value = matrix[row][col]
        # print(f'({row}, {col}) -> {value}')
        choice_index = preference_values.index(value)
        total_choice_index += choice_index
        choice_counts[choice_index] += 1

    for choice, count in sorted(choice_counts.items()):
        print(f"Students who got choice {choice + 1}: {count}")

    average_choice = total_choice_index / len(indexes)
    print(f"Average choice index: {average_choice:.2f}")

    end_time = time.perf_counter()
    print(f"Execution time: {end_time - start_time} seconds")