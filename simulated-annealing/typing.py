from typing import NamedTuple


class Course(NamedTuple):
    name: str
    capacity: int


class Preference(NamedTuple):
    course: Course
    weight: int


class Student(NamedTuple):
    name: str
    preferences: list[Preference]


class Assignment(NamedTuple):
    student: Student
    course: Course
