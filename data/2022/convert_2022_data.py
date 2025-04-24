import csv

with open('raw.csv', 'r') as f:
    reader = csv.reader(f)
    data = list(reader)

course_titles = []
for t in data[0][1:-1]:
    if t.startswith("DSEM Course Selection"):
        t = t[89:]
    course_titles.append(t)

new_data = [
    [""] + course_titles,
    [""] + [0 for _ in range(len(course_titles))]
]

print(new_data)

for row in data[1:]:
    new_row = [row[0]]
    for entry in row[1:-1]:
        if not entry:
            new_row.append(0)
        else:
            new_row.append(6-int(entry[0]))
    new_data.append(new_row)

# for i, row in enumerate(data):
#     preferred_courses = row[3:]
#     preferences = []
#     for course_title in course_titles:
#         if course_title in preferred_courses:
#             preferences.append(5-preferred_courses.index(course_title))
#         else:
#             preferences.append(0)
#     new_data.append([i]+preferences)

with open('0.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    for row in new_data:
        writer.writerow(row)