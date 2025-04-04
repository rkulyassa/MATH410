import csv
import math
import random


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


class SimulatedAnnealing:
    """
    Run the simulated annealing algorithm on a data set.

    Args:
        csv_file (str): The .csv file to read data from.
        preference_map (dict[int, int]): Optional, a mapping of raw csv values to custom values.
        initial_matching (dict[Student, Course]): Optional, start with a predefined matching.
        initial_temperature (float): Set the initial temperature, default 100.0
        cooling_rate (float): Set the cooling rate, default 0.99

    Attributes:
        students (list[Student]): The list of students to be assigned.
        courses (list[Course]): The list of courses to which students will be assigned.
        current_matching (dict[Student, Course]): The current assignment of students to courses.
        candidate_matching (dict[Student, Course]): The potential assignment to be compared to the current, each iteration.
        temperature (float): The current temperature.
        cooling_rate (float): The cooling rate, a fixed constant that scales the temperature each iteration.
    """
    def __init__(
        self,
        csv_file: str,
        preference_map: dict[int, int] = {},
        initial_matching: dict[Student, Course] = None,
        initial_temperature: float = 100.0,
        cooling_rate: float = 0.99
    ):
        with open(csv_file) as f:
            reader = csv.reader(f)
            rows = list(reader)

        self.preference_map = preference_map

        # Read courses from first 2 rows
        self.courses: list[Course] = []
        for course_name, course_capacity in zip(rows[0][1:], rows[1][1:]):
            course = Course(
                name=course_name.strip(),
                capacity=int(course_capacity)
            )
            self.courses.append(course)

        # Read student preferences from remaining rows
        self.students: list[Student] = []
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

            student = Student(
                name=student_name,
                preferences=preferences
            )
            self.students.append(student)

        # Use the initial matching if one was passed, otherwise generate random
        self.current_matching: dict[Student, Course] = {}
        if initial_matching:
            self.current_matching = initial_matching
        else:
            self.randomize_matching()

        # Set initial temperature and cooling rate
        self.temperature = initial_temperature
        self.cooling_rate = cooling_rate


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


    def print_stats(self) -> None:
        print("Stats for current matching:")
        print(f"Raw score: {self.eval_score(self.current_matching)}")

        # Determine how many students got their nth choices
        ranks = list(sorted(self.preference_map.values(), reverse=True))
        choices: list[int] = [0 for _ in range(len(ranks))]
        for student, course in self.current_matching.items():
            preference = student.preferences[course]
            rank = ranks.index(preference)
            choices[rank] += 1

        mean = 0
        total = sum(choices)
        for i, count in enumerate(choices):
            print(f"{count} students got choice {i} (score {ranks[i]})")
            mean += i * count / total
        print(f"On average students received choice {mean}")

        seats_filled: dict[Course, int] = {course: 0 for course in self.courses}
        for _, course in self.current_matching.items():
            seats_filled[course] += 1

        for course, seats in seats_filled.items():
            print(f"Course '{course.name}' filled {seats}/{course.capacity}")


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


    def solve(self, log_verbose: bool = False) -> None:
        # iterations = 200000
        iterations = 10000
        for i in range(iterations):
            if log_verbose:
                print("="*20)
                print(f"Iteration {i}")
                self.print_matching()

            # Set candidate to a shallow copy of the current
            self.candidate_matching = self.current_matching.copy()

            # Perform a random swap on the candidate
            student, course = self.random_swap()

            # Compare score of candidate with current
            current_score = self.eval_score(self.current_matching)
            candidate_score = self.eval_score(self.candidate_matching)
            delta = candidate_score - current_score
            if delta >= 0: # accept improvements
                if log_verbose:
                    print(f"Accepting swap of student '{student.name}' to course '{course.name}', improving the score by {delta}")
                self.current_matching = self.candidate_matching
            else: # accept worse candidates on temperature-conditioned probability
                # acceptance_probability = math.exp(delta / self.temperature)
                acceptance_probability = delta / self.temperature
                if random.random() < acceptance_probability:
                    self.current_matching = self.candidate_matching
                    if log_verbose:
                        print(f"Accepting bad swap of student '{student.name}' to course '{course.name}' with probability {acceptance_probability}, decreasing the score by {delta}")
                elif log_verbose:
                    print(f"Rejecting swap of student '{student.name}' to course '{course.name}', which would decrease the score by {delta}")

            self.temperature *= self.cooling_rate
            if log_verbose:
                print(f"Temperature cooling to {self.temperature}")

            progress_str = f"I: {i}"
            score_str = f"F: {current_score}"
            temperature_str = f"T: {self.temperature}"
            acceptance_probability_str = f"P: {delta / self.temperature}"
            if i % 1000 == 0:
                print(f"{progress_str.ljust(20)} | {score_str.ljust(20)} | {temperature_str.ljust(25)} | {acceptance_probability_str.ljust(20)}")
            else:
                print(f"{progress_str.ljust(20)} | {score_str.ljust(20)} | {temperature_str.ljust(25)} | {acceptance_probability_str.ljust(20)}", end="\r")


    def output_csv_for_ha(self, out_path: str) -> None:
        seats_filled: dict[Course, int] = {course: 0 for course in self.courses}
        for _, course in self.current_matching.items():
            seats_filled[course] += 1

        with open(out_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([","] + [course.name for course in self.courses])
            writer.writerow([","] + [seats_filled[course] for course in self.courses])
            for student in self.students:
                writer.writerow([student.name] + [-student.preferences[course] for course in self.courses])

        print(f"Wrote output minimization matrix to {out_path}")