import unittest

from annealing.annealing import *
from annealing.typing import *

c1 = Course("C1", 3)
c2 = Course("C2", 2)
c3 = Course("C3", 2)

courses: list[Course] = [c1, c2, c3]

ana = Student("Ana", [Preference(c1, 3), Preference(c2, 2), Preference(c3, 1)])
bob = Student("Bob", [Preference(c1, 1), Preference(c2, 2)])
cat = Student("Cat", [Preference(c2, 1), Preference(c3, 3)])
dan = Student("Dan", [Preference(c1, 3), Preference(c2, 1), Preference(c3, 2)])
eva = Student("Eva", [Preference(c1, 3), Preference(c2, 1), Preference(c3, 2)])
fry = Student("Fry", [Preference(c1, 2), Preference(c2, 3), Preference(c3, 1)])

students: list[Student] = [ana, bob, cat, dan, eva, fry]

matchings: list[list[Match]] = [
    [
        Match(ana, c1),
        Match(bob, c2),
        Match(cat, c3),
        Match(dan, c1),
        Match(eva, c3),
        Match(fry, c2),
    ],
    [
        Match(ana, c2),
        Match(bob, c3),
        Match(cat, c3),
        Match(dan, c1),
        Match(eva, c1),
        Match(fry, c1),
    ],
    [
        Match(ana, c3),
        Match(bob, c1),
        Match(cat, c1),
        Match(dan, c3),
        Match(eva, c2),
        Match(fry, c2),
    ],
]


class TestAnnealing(unittest.TestCase):
    def test_course_full(self):
        self.assertEqual(course_full(matchings[0], c1), False)
        self.assertEqual(course_full(matchings[1], c1), True)
        self.assertEqual(course_full(matchings[2], c3), True)

    def test_random_matching(self):
        matching = random_matching(students, courses)
        self.assertIsInstance(matching, list)
        for match in matching:
            self.assertIsInstance(match, Match)

    def test_total_score(self):
        self.assertEqual(total_score(matchings[0]), 16)
        self.assertEqual(total_score(matchings[1]), 13)
        self.assertEqual(total_score(matchings[2]), 8)

    def test_annealing(self):
        result = annealing(students, courses, logging=True)
        print_matching(result)


if __name__ == "__main__":
    unittest.main()
