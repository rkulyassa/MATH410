import csv
import math
import random
# from typing import NamedTuple


class Course:
    """
    Represents a singular course.

    Attributes:
        name (str): The unique name or identifier of the course.
        capacity (int): The maximum number of students that can be assigned to the course.
    """
    def __init__(self, name: str, capacity: int):
        self.name = name
        self.capacity = capacity

    def __str__(self):
        return f"Course '{self.name}' with capacity {self.capacity}"


# class Preference(NamedTuple):
#     """
#     Represents a student's preference for a course with a integer value.
#     """
#     course: Course
#     weight: int


class Student:
    """
    Represents an individual student.

    Attributes:
        name (str): The unique name or identifier of the student.
        preferences (dict[Course, int]): A mapping of the student's preference for each course.
    """
    def __init__(self, name: str, preferences: dict[Course, int]):
        self.name = name
        self.preferences = preferences

    def __str__(self):
        sorted_preferences = dict(sorted(self.preferences.items(), key=lambda p: -p[1]))
        preferences_str = ", ".join([f"'{course.name}' ({weight})" for course, weight in sorted_preferences.items()])
        return f"Student '{self.name}' with preferences {preferences_str}"

# class Assignment(NamedTuple):
#     """
#     Represents the assignment of a student to a course.
#     """
#     student: Student
#     course: Course

class SimulatedAnnealing:
    """
    Run the simulated annealing algorithm on a data set.

    Attributes:
        students (list[Student]): The list of students to be assigned.
        courses (list[Course]): The list of courses to which students will be assigned.
        current_matching (dict[Student, Course]): The current assignment of students to courses.
        candidate_matching (dict[Student, Course]): The potential assignment to be compared to the current, each iteration.
    """
    def __init__(self, csv_file: str, preference_map: dict[int, int] = {}):
        with open(csv_file) as f:
            reader = csv.reader(f)
            rows = list(reader)

        self.students: list[Student] = []
        self.courses: list[Course] = []
        self.current_matching: dict[Student, Course] = {}

        # Read courses from first 2 rows
        for course_name, course_capacity in zip(rows[0][1:], rows[1][1:]):
            course = Course(
                name=course_name.strip(),
                capacity=int(course_capacity)
            )
            self.courses.append(course)

        # Read student preferences from remaining rows
        for row in rows[2:]:
            student_name = row[0]
            preferences: dict[Course, int] = {}

            for i, val in enumerate(row[1:]):
                if val:
                    val = int(val)
                    # apply the custom weight if applicable
                    preference = preference_map[val] if val in preference_map else val
                else: # treat empty cells as 0
                    preference = 0

                preferences[self.courses[i]] = preference

                # preference = Preference(
                #     course=self.courses[i],
                #     weight=preference_weight
                # )
                # preferences.append(preference)

            student = Student(
                name=student_name,
                preferences=preferences
            )
            self.students.append(student)

    def course_full(self, course: Course) -> bool:
        current = sum(c == course for c in self.current_matching.values())
        return current >= course.capacity

    def randomize_matching(self) -> None:
        for student in self.students:
            while True:
                course = random.choice(self.courses)
                if not self.course_full(course):
                    self.current_matching[student] = course
                    break

    @staticmethod
    def eval_score(matching: dict[Student, Course]) -> int:
        """
        Gets the raw score of a matching, by summing each student's preference for their respective assignment.
        """
        return sum(student.preferences[course] for student, course in matching.items())
    
    # @staticmethod
    # def eval_objective(matching: dict[Student, Course]) -> int:


    def print_matching(self) -> None:
        for student, course in self.current_matching.items():
            print(f"'{student.name}' -> '{course.name}' ({student.preferences[course]})")
        print(f"Raw score: {self.eval_score(self.current_matching)}")

    def random_swap(self) -> tuple[Student, Course]:
        """
        Performs a random swap on the current candidate matching.

        Returns:
            A tuple[Student, Course] representing the new assignment resulting from the swap.
        """

        student = random.choice(self.students)

        while True:
            new_course = random.choice(self.courses)
            if not self.course_full(new_course) and new_course != self.current_matching[student]:
                self.candidate_matching[student] = new_course
                return (student, new_course)

    def solve(
        self,
        initial_matching: dict[Student, Course] = None,
        initial_temperature: float = 100,
        cooling_rate: float = 0.99,
    ) -> None:

        # Use the initial matching if one was passed, otherwise generate random
        if initial_matching:
            self.current_matching = initial_matching
        else:
            self.randomize_matching()

        for i in range(100000):
            # self.print_matching()

            # Set candidate to a shallow copy of the current
            self.candidate_matching = self.current_matching.copy()

            # Perform a random swap on the candidate
            student, course = self.random_swap()

            # Compare score of candidate with current
            current_score = self.eval_score(self.current_matching)
            candidate_score = self.eval_score(self.candidate_matching)
            if candidate_score > current_score:
                # print(f"Accepting swap of student '{student.name}' to course '{course.name}', improving the score by {candidate_score - current_score}")
                self.current_matching = self.candidate_matching
            else:
                pass
                # print(f"Rejecting swap of student '{student.name}' to course '{course.name}', which would decrease the score by {candidate_score - current_score}")





if __name__ == "__main__":
    preference_map = {
        0: -100,
        1: 5,
        2: 10,
        3: 20
    }
    sa = SimulatedAnnealing("./data/trivial.csv", preference_map=preference_map)

    # for course in sa.courses:
    #     print(course)
    # for student in sa.students:
    #     print(student)
    sa.solve()
    sa.print_matching()


