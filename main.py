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
        max_iterations=5000,
        temperature=100,
        cooling_rate=0.99,
    )
    # print_matching(result)
    final_score = eval_score(result)
    spread = calculate_spread(result, True)

    print("Final score (modified):", final_score)
    print("Final score (raw):", final_score + spread)

    print("Final variance:", spread)

    # print_matching(result)
    # for match in result:
    #     student_preferences = match.student.preferences
    #     # for preference in student_preferences:
    #     if match.course in [p.course for p in student_preferences]:
    #         for preference in student_preferences:
    #             if preference.course == match.course:
    #                 print(preference.weight)
    #     else:
    #         print("Bad")


if __name__ == "__main__":
    main()
