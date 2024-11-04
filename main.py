import csv

from annealing.annealing import *
from annealing.typing import *


def main():
    with open("data/FA22.csv") as f:
        reader = csv.reader(f)
        rows = list(reader)

    students: list[Student] = []
    courses: list[Course] = [Course(entry, 20) for entry in rows[0][1:]]

    for row in rows[1:]:
        name = row[0]
        preferences: list[Preference] = []

        for i, entry in enumerate(row[1:]):
            entry = entry.strip()
            if not entry:
                continue
            weight = int(entry)
            preference = Preference(courses[i], weight)
            preferences.append(preference)

        student = Student(name, preferences)
        students.append(student)

    # print("Number of courses:", len(courses))
    # print("Number of students:", len(students))

    result = annealing(
        students,
        courses,
        logging=False,
        max_iterations=50000,
        temperature=100,
        cooling_rate=0.99,
    )
    # print_matching(result)
    print("Final score:", total_score(result))


if __name__ == "__main__":
    main()
