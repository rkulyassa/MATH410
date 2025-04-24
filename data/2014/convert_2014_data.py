import csv

with open('raw.csv', 'r') as f:
    reader = csv.reader(f)
    data = list(reader)

course_titles = []
for row in data:
    course_titles += row[:5]
course_titles = list(set(course_titles))

print(course_titles)

new_data = [
    [""] + course_titles,
    [""] + [0 for _ in range(len(course_titles))]
]

for row in data:
    student_id = row[8]
    preferred_courses = row[:5]
    preferences = []
    for course_title in course_titles:
        if course_title in preferred_courses:
            preferences.append(5-preferred_courses.index(course_title))
        else:
            preferences.append(0)
    new_data.append([student_id]+preferences)

# print(new_data)

with open('data/2014/0.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    for row in new_data:
        writer.writerow(row)