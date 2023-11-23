import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Replace this with your file path
file_path = '/home/picchai/Documents/GItHub/resluts_automation_ByScrapping/STORE/Results_meta.csv'

# Read the CSV file
data = pd.read_csv(file_path)

# Extract subjects
subjects = data.columns[3:-2]

# Count number of students
num_students = len(data)

# Define the grade points order
grade_points_order = {"O": 10, "A+": 9, "A": 8, "B+": 7, "B": 6, "C": 5, "P": 4, "F": 0}

# Initialize a dictionary to store grade counts and top students for each subject
grade_counts = {subject: {} for subject in subjects}
top_students = {subject: None for subject in subjects}

# Iterate through rows and count grades for each subject
for _, row in data.iterrows():
    for subject in subjects:
        cell_value = row[subject]
        if not isinstance(cell_value, str):
            # Handling non-string values
            cell_value = str(cell_value)
        marks_and_grade = cell_value.split()
        grade = marks_and_grade[1] if len(marks_and_grade) == 2 else 'NA'
        if grade not in grade_counts[subject]:
            grade_counts[subject][grade] = 0
        grade_counts[subject][grade] += 1

        # Update top student for each subject
        if top_students[subject] is None or grade_points_order.get(grade, -1) > grade_points_order.get(
                top_students[subject][1], -1):
            top_students[subject] = (row['USN'], marks_and_grade[0], grade) if len(marks_and_grade) == 2 else (
            row['USN'], 'NA', grade)
# Calculate the highest number of failures for each subject
failures = {}
for subject, counts in grade_counts.items():
    failures[subject] = counts.get('F', 0)

# Sort subjects by the number of failures
sorted_failures = {k: v for k, v in sorted(failures.items(), key=lambda item: item[1], reverse=True)}

# Generate colors using a range between 0 and 1 for failures chart
color_values_failures = np.linspace(0, 1, len(sorted_failures))

# Bar chart for the highest number of failures across subjects with RGB colors
plt.figure(figsize=(8, 6))
bars_failures = plt.bar(sorted_failures.keys(), sorted_failures.values(), color=plt.cm.gist_rainbow(color_values_failures))
plt.xlabel('Subjects')
plt.ylabel('Number of Failures')
plt.title('Highest Number of Failures across Subjects')

# Displaying counts on top of bars and total number of students
for bar, count in zip(bars_failures, sorted_failures.values()):
    plt.text(bar.get_x() + bar.get_width() / 2, count, str(count),
             ha='center', va='bottom', fontsize=9)

plt.text(0.5, max(sorted_failures.values()) + 5, f'Total Students: {num_students}',
         ha='center', fontsize=9, style='italic')

plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

# Plotting bar charts for each subject
for subject in subjects:
    # Ensure all grade keys exist even if their counts are zero
    for grade in grade_points_order.keys():
        if grade not in grade_counts[subject]:
            grade_counts[subject][grade] = 0

    sorted_grades = sorted(grade_counts[subject].items(), key=lambda x: grade_points_order.get(x[0], -1), reverse=True)
    grades = [grade[0] for grade in sorted_grades]
    counts = [grade[1] for grade in sorted_grades]

    # Generate colors using the same range as failures chart for consistency
    color_values = np.linspace(0, 1, len(grades))

    plt.figure(figsize=(8, 6))
    bars = plt.bar(grades, counts, color=plt.cm.gist_rainbow(color_values))
    plt.xlabel('Grades')
    plt.ylabel('Number of Students')
    plt.title(f'Grade Distribution for {subject}')

    # Displaying counts on top of bars and total number of students
    max_count = max(counts)
    text_offset = max_count * 0.02  # Adjust the text offset based on the maximum count

    for bar, count in zip(bars, counts):
        if count > 0:
            plt.text(bar.get_x() + bar.get_width() / 2, count + text_offset, str(count),
                     ha='center', va='bottom', fontsize=9)

    # Display the top student (USN, Marks, Grade) for each subject
    top_student = top_students[subject]
    plt.text(0.5, -2, f'Top Student: USN {top_student[0]} ({top_student[1]} {top_student[2]})',
             ha='center', fontsize=9, style='italic')
    plt.text(0.5, -3, f'Total Students: {num_students}', ha='center', fontsize=9, style='italic')

    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()
