import math
import random

from .typing import Course, Match, Student


def print_matching(matching: list[Match]) -> None:
    for match in matching:
        print(f"{match.student.name} -> {match.course.name}")


def course_full(matching: list[Match], target_course: Course) -> bool:
    count = 0
    for _, course in matching:
        if course == target_course:
            count += 1
        if count >= target_course.capacity:
            return True
    return False


def random_matching(
    students: list[Student], courses: list[Course]
) -> list[Match]:
    matching: list[Match] = []
    for student in students:
        course = random.choice(courses)
        while course_full(matching, course):
            course = random.choice(courses)
        match = Match(student, course)
        matching.append(match)
    return matching


# FIX: should be based on percentage filled rather than just number of students


def calculate_spread(matching: list[Match], print_spread: bool = False) -> float:
    filled_seats: dict[Course, float] = {}

    for _, course in matching:
        if course in filled_seats:
            filled_seats[course] += 1 / course.capacity
        else:
            filled_seats[course] = 1 / course.capacity

    mean = sum(filled_seats.values()) / len(filled_seats)

    sum_squares = sum([(v - mean) ** 2 for v in filled_seats.values()])
    variance = sum_squares / len(filled_seats)

    if print_spread:
        for course in filled_seats:
            print(f"{course} assigned {round(filled_seats[course] * course.capacity)} students")

    return variance


def eval_penalty(matching: list[Match]) -> float:
    weight_factor = 7000
    spread = calculate_spread(matching)
    # print(spread)
    return spread * weight_factor


def eval_score(matching: list[Match]) -> int:
    total_score = 0
    for student, course in matching:
        preference = next(
            (p for p in student.preferences if p.course == course), None
        )
        if preference:
            total_score += preference.weight

    return total_score

def init_data() -> None:
    

def random_swap(
    matching: list[Match],
    students: list[Student],
    courses: list[Course],
    max_tries: int | None = None,
) -> list[Match]:
    new_matching = matching.copy()
    student = random.choice(students)
    index = next(i for i, m in enumerate(new_matching) if m.student == student)
    match = new_matching[index]
    course = random.choice(courses)
    tries = 0
    while course_full(new_matching, course) or course == match.course:
        course = random.choice(courses)
        tries += 1
        if max_tries and tries >= max_tries:
            return new_matching
    # print(f"Moved {student.name} from {match.course.name} to {course.name}")
    new_matching[index] = match._replace(course=course)
    return new_matching


def annealing(
    students: list[Student],
    courses: list[Course],
    initial_matching: list[Match] = None,
    temperature: float = 100,
    cooling_rate: float = 0.99,
    max_iterations: int = 1000,
    logging: bool = False,
) -> list[Match]:
    if not initial_matching:
        initial_matching = random_matching(students, courses)

    current_matching = initial_matching
    current_score = eval_score(current_matching) - eval_penalty(
        current_matching
    )

    for i in range(max_iterations):
        if logging:
            print(
                "Iteration",
                str(i).ljust(2),
                "| Score",
                str(current_score).ljust(2),
                "| Temperature",
                str(round(temperature, 4)),
            )

        new_matching = random_swap(
            current_matching, students, courses, max_tries=5
        )
        new_score = eval_score(new_matching) - eval_penalty(new_matching)
        # print_matching(new_matching)
        # print("New score:", new_score)

        if new_score > current_score:
            current_matching = new_matching
            current_score = new_score
        else:
            delta = new_score - current_score
            acceptance_probability = math.exp(delta / temperature)
            if random.random() < acceptance_probability:
                current_matching = new_matching
                current_score = new_score

        temperature *= cooling_rate

    return current_matching
