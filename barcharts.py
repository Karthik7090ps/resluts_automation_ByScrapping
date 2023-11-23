import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import os
from fpdf import FPDF

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

# Create a directory to save charts if it doesn't exist
charts_directory = '/home/picchai/Documents/GItHub/resluts_automation_ByScrapping/charts/'
if not os.path.exists(charts_directory):
    os.makedirs(charts_directory)

# Plotting bar charts for each subject and save as PNG
chart_paths = []
for subject in subjects:
    # Ensure all grade keys exist even if their counts are zero
    for grade in grade_points_order.keys():
        if grade not in grade_counts[subject]:
            grade_counts[subject][grade] = 0

    sorted_grades = sorted(grade_counts[subject].items(), key=lambda x: grade_points_order.get(x[0], -1), reverse=True)
    grades = [grade[0] for grade in sorted_grades]
    counts = [grade[1] for grade in sorted_grades]

    # Generate colors using a range between 0 and 1
    color_values = np.linspace(0, 1, len(grades))

    plt.figure(figsize=(8, 6))
    bars = plt.bar(grades, counts, color=plt.cm.viridis(color_values))
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

    # Display the top student (USN, Marks, Grade) for each subject in the top right corner
    top_student = top_students[subject]
    plt.text(0.95, 0.95, f'Top Student: USN {top_student[0]} ({top_student[1]} {top_student[2]})',
             ha='right', va='top', fontsize=9, transform=plt.gca().transAxes)
    plt.text(0.95, 0.90, f'Total Students: {num_students}',
             ha='right', va='top', fontsize=9, transform=plt.gca().transAxes)

    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    
    # Save the bar chart as PNG
    chart_path = os.path.join(charts_directory, f'{subject}_chart.png')
    plt.savefig(chart_path)
    plt.close()
    chart_paths.append(chart_path)

# Convert all PNG charts into a single PDF
def convert_png_to_pdf(png_files, output_pdf):
    page_width = 640  # 640 pixels
    page_height = 480  # 480 pixels
    # Create a PDF object
    pdf = FPDF(orientation='P', unit='pt', format=(page_width, page_height))
    # Add each image as a page in the PDF
    for image in png_files:
        pdf.add_page()
        pdf.image(image, x=0, y=0, w=page_width, h=page_height, type='PNG', link=image)  # Specify type and link to maintain image quality
        pdf.image("watermark.png", x=page_width - 50, y=page_height - 50, w=40, h=30, type='PNG')

    # Save the PDF file
    pdf.output(output_pdf)

# Call the function to convert PNGs to PDF
output_pdf_path = '/home/picchai/Documents/GItHub/resluts_automation_ByScrapping/Dept_Analysis.pdf'
convert_png_to_pdf(chart_paths, output_pdf_path)
