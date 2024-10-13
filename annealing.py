import random
import math
from data import S, C

# ST = {
#     'Lee': {'M': 3, 'A': 2},
#     'Becker': {'A': 2, 'M': 1},
#     'Cirelli': {'A': 2, 'M': 2}
# }
# CT = {
#     'M': 3,
#     'A': 3
# }
# M = {
#     'Lee': 'A',
#     'Becker': 'A',
#     'Cirelli': 'A'
# }
# print(course_full(M, CT, 'M'))

def random_course(courses: dict) -> str:
    return random.choice(list(courses.keys()))

def random_student(students: dict) -> str:
    return random.choice(list(students.keys()))

def course_full(matching: dict, courses: dict, target_course: str) -> bool:
    capacity = courses[target_course]
    count = 0
    for course in matching.values():
        if course == target_course:
            count += 1
        if count >= capacity:
            return True
    return False

def random_matching(students: dict, courses: dict) -> dict:
    matching = {}
    for student in students.keys():
        course = random_course(courses)
        while course_full(matching, courses, course):
            course = random_course(courses)
        matching[student] = course
    return matching

def total_score(students: dict, matching: dict):
    total_score = 0
    for student, course in matching.items():
        try:
            score = students[student][course]
        except KeyError:
            score = 0
        total_score += score
    return total_score

def random_swap(matching: dict, students: dict, courses: dict):
    new_matching = matching.copy()
    student = random_student(students)
    new_course = random_course(courses) # restrict to just courses that the student has?
    while course_full(matching, courses, new_course) or new_course == matching[student]:
        new_course = random_course(courses)
    new_matching[student] = new_course
    return new_matching

def simulated_annealing(
        students: dict,
        courses: dict,
        initial_matching: dict = None,
        temperature: float = 1000,
        cooling_rate: float = 0.99,
        max_iterations: int = 1000,
        logging: bool = False) -> dict:
    
    if not initial_matching:
        initial_matching = random_matching(students, courses)

    current_matching = initial_matching
    current_score = total_score(students, current_matching)

    for i in range(max_iterations):
        if logging: print('Iteration', str(i).ljust(2), '| Score', str(current_score).ljust(2), '| Temperature', str(temperature))
        new_matching = random_swap(current_matching, students, courses)
        new_score = total_score(students, new_matching)

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

if __name__ == '__main__':
    result = simulated_annealing(S, C)
    print(result)
    print(total_score(S, result))