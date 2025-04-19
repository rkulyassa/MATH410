import csv

with open('2018 DSEM Assignments.xlsx - Registration Form.csv', 'r') as f:
    reader = csv.reader(f)
    data = list(reader)

override_map = {
    "Magic Bullets: The role and Limitations of Science in Medicine: Adam Cassano": "Magic Bullets: The Role and Limitations of Science in Medicine, Prof. Adam Cassano",
    "Forty Studies that Changed Psychology": "Forty Studies That Changed Psychology, Prof. Patrick Dolan",
    "Forty Studies That Changed Psychology: Patrick Dolan": "Forty Studies That Changed Psychology, Prof. Patrick Dolan",
    "Weapons of Math Destruction: Living with Algorithms, Prof. Minjoon Kouth": "Weapons of Math Destruction: Living with Algorithms, Prof. Minjoon Kouh",
    "Why We Buy; the Science of Shopping": "Why We Buy: The Science of Shopping, Prof. Chris Andrews"
}

course_titles = []
for row in data[1:]:
    courses = row[3:]
    for i, course in enumerate(row[3:]):
        if course in override_map:
            courses[i] = override_map[course]
        if course.endswith("Selection"):
            courses.remove(course)
    course_titles += courses
course_titles = list(set(course_titles))

new_data = [
    [""] + course_titles,
    [""] + [0 for _ in range(len(course_titles))]
]

for i, row in enumerate(data):
    preferred_courses = row[3:]
    preferences = []
    for course_title in course_titles:
        if course_title in preferred_courses:
            preferences.append(5-preferred_courses.index(course_title))
        else:
            preferences.append(0)
    new_data.append([i]+preferences)

with open('0.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    for row in new_data:
        writer.writerow(row)