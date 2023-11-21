#!/usr/bin/python3


"""
*****************************************************************************************
*
*        		===============================================
*           		    EDUCATIONAL PURPOSE ONLY
*        		===============================================
*
*  This script shows the usage and working of Web scrapping
*
* The website that is shown here is used only for educational purpose only
*
*****************************************************************************************
# Author: karthik P S
# Department of Electronics and Communication Engineering
# Email: Karthikreddyr7@gmail.com

"""                                                                                           
# this is the completely developing code
import json 
import os
import cv2
import time
import csv
import pandas
import numpy as np
import dateutil
from PIL import Image
from selenium import webdriver
import matplotlib.pyplot as plt
from pytesseract import pytesseract
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from tkinter import simpledialog 
from tkinter import messagebox
import subprocess
from fpdf import FPDF

dateutil.__version__ = "2.8.1"

start_time = time.time()

# enable the below function to make the json file editable in the interface
enable_JSON_PANEL= 0

if enable_JSON_PANEL==0:
    path = 'n'
else:
    path = simpledialog.askstring("Input","Edit JSON File? Y/N (Default No): ")

if path is None or path =="":
    path = 'n'

if path.lower() == 'y':
    file_path = "/home/picchai/Documents/GItHub/resluts_automation_ByScrapping/config.json"
    subprocess.call(["nano", file_path])

with open("/home/picchai/Documents/GItHub/resluts_automation_ByScrapping/config.json", "r") as config_file:
    config = json.load(config_file)

dev = config["developer_mode"]
print_v=config["print_debug_data"]
led=config["screen_show"]

if dev==0:
    messagebox.showinfo("WELCOME", "Automated student Result___Analysis Tool")
    messagebox.showinfo("THANKYOU", "Developed by Karthik P S, __Dept. of EC, BMSCE__")

if led==0:
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)                     #DRIVER FOR CHROME SELENIUM
else:
     driver = webdriver.Chrome()

# FUNCTION TO READ TECXT FROM CAPTCHA
def read_text():
    captcha_image = config["captcha_image"]
    img = cv2.imread(captcha_image)
    gry = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    (h, w) = gry.shape[:2]
    gry = cv2.resize(gry, (w, h))
    cls = cv2.morphologyEx(gry, cv2.MORPH_CLOSE, None)
    thr = cv2.threshold(cls, 200, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    thr = cv2.GaussianBlur(thr, (3, 3), 0) 
    kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
    thr = cv2.filter2D(thr, -2, kernel)
    custom_config = r'--oem 3 --psm 6'# -c tessedit_char_whitelist=0123456789abcdefghijklmnopqrsuvwxyz'
    captcha = pytesseract.image_to_string(thr, config=custom_config)
    # cv2.imshow('Original Image',thr)
    # cv2.waitKey(0)
    os.remove(captcha_image)
    return captcha

#FUNCTION TO DOWNLOAD CAPTCHA FROM THE BROWSER (PRINTSCREEN METHOD)
def get_captcha():
    captcha_fn = config["captcha_image"]
    element = driver.find_element(By.ID, "captcha_image")
    location = element.location
    size = element.size
    temp=config["temp_png_location"]
    driver.save_screenshot(temp)
    if print_v==1:
        print("screenshot taken")
    x = location['x']
    y = location['y']
    w = size['width']
    h = size['height']
    width = x + w-10
    height = y + h

    im = Image.open(temp)
    im = im.crop((int(x), int(y), int(width), int(height)))
    im.save(captcha_fn)
    if print_v==1:
        print("image downloaded")

# FUNCTION TO CREATE RADAR CHART
def create_radar_chart(usn, grades, sub,student_name):
    # Define the grade mapping
    grade_mapping = {
        'O': 10,
        'A+': 9,
        'A': 8,
        'B+': 7,
        'B': 6,
        'C': 5,
        'P': 4,
        'F': 0
    }

    # Filter out subjects with grades '-' and 'PP'
    filtered_grades = []
    filtered_sub = []
    for grade, subject in zip(grades, sub):
        if grade not in ['-', 'PP']:
            filtered_grades.append(grade)
            filtered_sub.append(subject)

    if not filtered_grades:
        print("No valid data to create a radar chart for USN:", usn)
        return None

    num_subjects = len(filtered_sub)

    labels = filtered_sub
    angles = np.linspace(0, 2 * np.pi, num_subjects, endpoint=False).tolist()

    # Initialize an empty list to store values for plotting
    values = []

    for grade in filtered_grades:
        grade_value = grade_mapping.get(grade, 0)  # Use the grade mapping
        values.append(grade_value)

    fig, ax = plt.subplots(subplot_kw=dict(polar=True))

    # Draw radial lines
    for angle in angles:
        ax.plot([0, angle], [0, max(values)], color='g', linewidth=1, linestyle='--') #colour of radial line

    # Draw the border of the radar chart by plotting a polygon
    border = plt.Polygon(np.column_stack([angles, values]), edgecolor='k', linewidth=2, closed=True, fill=False)
    ax.add_patch(border)

    # Plot the radar chart
    ax.fill(angles, values, 'g', alpha=0.1) #change letter for colour 'g' for green
    ax.set_yticklabels([])

    # Set the radial grid lines
    ax.set_xticks(angles)
    ax.set_xticklabels(labels)

    ax.set_title(f'{usn} - {student_name}')

    # Plot grades with points
    for angle, value, grade in zip(angles, values, filtered_grades):
        x, y = np.cos(angle), np.sin(angle)
        ax.plot(angle, value, 'go', markersize=6)  # Plot the grade point #GRDE g for green and o for circle
        ax.text(angle, value, grade, ha='center', va='bottom')
        ax.text(angle, value, grade, ha='center', va='bottom', fontweight='bold')

    radar_chart_filename = config["radar_save"].replace("{{usn}}", usn)
    plt.savefig(radar_chart_filename)  # Removed bbox_inches='tight'

    plt.close()

    return radar_chart_filename

#MAIN FUNCTION OF THE CODE TO GET RESULTS
def main():

    #SPECIFY THE PATH OF CSV FILE
    filename = config["csv_path"] #'/home/picchai/result_automation_system/result/EC_3rd_sem_result.csv'

    # EDIT AS PER GRADE POINTS (VTU BASED)
    grade_points = config["grade_points"] 

    # EDIT SUBJECT CREDITS BASED ON SUBJECTS (EDIT IS REQUIRED FOR EACH SEM)
    subject_credits = config["subject_credits"] 



    # OPENING A CSV FILE FOR UPDATING MARKS
    with open(filename, 'w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)

        # driver.get("https://www.google.com/")
        # driver.implicitly_wait(0.5)
        
        # INITIALIZE PARAMETERS
        if dev==1:
            path='a'
        else:    
            path = simpledialog.askstring("Input", "Auto config or Manual config A/M")
        if path is None or path =="":
            path = 'A'
        if path.lower()=='a':
            auto = 1
        else:
            auto = 0
        auto = config["auto"] or auto 
        if auto == 0:
            user_input = simpledialog.askstring("Input", "Enter the starting number of USN (DEFAULT: 400):")
            firstnum = int(user_input) if user_input else 400

            user_input = simpledialog.askstring("Input","Enter the last USN number (DEFAULT: 423): ")
            lastusn = int(user_input) if user_input else 423

            # status = simpledialog.askstring("Input","Infinite loop of Captcha Y/N: ")
            # if status is None or status =="":
            #     status = 'y'
            status = 'y'

            if status.lower() == 'n':
                user_input = simpledialog.askstring("Input","Enter the maximum attempts (DEFAULT: 6):")
                max_attempts = int(user_input) if user_input else 6

            user_input = simpledialog.askstring("Input","Enter the branch number (DEFAULT: 1bm22ec): ")
            usn_num = user_input if user_input else "1bm22ec"
        else:
            firstnum = config["firstnum"]
            lastusn = config["lastusn"]
            usn_num = config["usn_num"]
            status = config["status"]


        data = []
        heading = 0
        credits=0
        radar_chart_list = []
        write_path=config["write_radarpath"]

        driver.get(config["result_link"])
        driver.implicitly_wait(0.5)
        time.sleep(2)


        # RUN THE CODE UNTILL THE LIMIT FOR USN REACHES

        while True:

            captcha_attempts=0
            captcha_solved=False

                # set rollnumber
            usn_number = usn_num+str(firstnum)

            driver.find_element(By.XPATH, '//*[@id="usn"]').clear()
            driver.find_element(By.XPATH, '//*[@id="usn"]').send_keys(usn_number)
            time.sleep(2)


            # WHILE CAPTCHA IS WRONG TRY AGAIN BY REFRESHING SITE
            while not captcha_solved:
                break_loop = False
                # if status.lower() == 'n' :
                #     if max_attempts - captcha_attempts == 0:
                #         break
                get_captcha()
                captcha1 = read_text()
                if print_v==1:
                    print("Captcha Attempt", captcha_attempts + 1, ":", captcha1)


                driver.find_element(By.ID, "captcha").send_keys(captcha1)
                time.sleep(1)
                driver.find_element(By.XPATH, '//*[@id="showBtn"]').send_keys(Keys.ENTER)
                time.sleep(2)

                # check if result page is opened
                elements = driver.find_elements(By.XPATH,  '//*[@id="res"]/h4[@class="text-center text-danger"]')
                for element in elements:
                    if "Invalid USN" in element.text:
                        break_loop = True

                if break_loop:
                    break

                if "Student Name" in driver.page_source:
                    captcha_solved = True
                
                else:
                    # Captcha is incorrect, clear input fields and try again
                    driver.find_element(By.XPATH, '//*[@id="captcha"]').clear()
                    print("Captcha is incorrect, trying again...")
                    captcha_attempts += 1


            # IF CAPTCHA IS CORRECTLY ENTERED
            if captcha_solved:
                print("captcha solved successfully")


                ###################### EXTRACT THE DATA FROM WEB
                table = driver.find_element(By.XPATH, '//*[@id="printTable"]')
                student_name_element = driver.find_element(By.XPATH, '//*[@id="printTable"]/thead/tr[2]/th[2]')
                usn_element = driver.find_element(By.XPATH, '//*[@id="printTable"]//tr[th[contains(text(), "USN")]]/th')

                # Extract the text from the elements
                student_name = student_name_element.text.strip()
                student_name = student_name.split(':')[1].strip()
                usn = usn_element.text.strip()
                usn = usn.split(':')[1].strip()
                if print_v==1:
                    # Print the extracted student name and USN
                    print(f"Student Name: {student_name}")
                    print(f"USN: {usn}")
                data = []
                ###############################################################

                rows = table.find_elements(By.TAG_NAME, 'tr')
                for row in rows:
                    cols = row.find_elements(By.TAG_NAME, 'td')
                    cols_data = [col.text.strip() for col in cols]
                    data.append(cols_data)
                print(data)
                ######################### DO NOT EDIT ABOVE LINES ####################

                # FUNCTION CALL TO CALCULATE SGPA AND CREDITS
                sgpa,credits = calculate_sgpa(data, grade_points, subject_credits)  # Calculate SGPA
                sgpa = round(sgpa, 2)  # Round to 2 decimal places

                data = data[1:]
                if heading == 0:
                    sub = []
                    sub = shorten_name(data)

                    if write_path==1:
                        header = ["USN", "Student Name"] + sub + [ "CREDIT_POINTS","SGPA", "    CHART    "]
                    else:
                        header = ["USN", "Student Name"] + sub + [ "CREDIT_POINTS","SGPA"]

                    csv_writer.writerow(header)
                    heading = 1

                usn_data = [usn, student_name] + [""] * (len(sub) + 2)  # Initialize with empty strings, including space for "Grade" and "SGPA"
                total_values = []

                for row in data:
                    if row:
                        marks = row[4]  # Assuming that the 5th column is the total marks
                        grade = row[5]  # Assuming that the 6th column is the grade
                        formatted_data = f"{marks}  {grade}"
                        total_values.append(formatted_data)

                for i in range(len(sub)):
                    usn_data[i + 2] = total_values[i] if i < len(total_values) else ""  # Filling Total for the respective subject

                # EXTRA ROW DATA CAN BE ADDED HERE
                usn_data[-1] = sgpa  # Adding "SGPA" value
                usn_data[-2] = credits 

####################################################################################################################

                radar_chart_filename = create_radar_chart(usn, [row[5] for row in data if len(row) >= 6],sub,student_name)
                radar_chart_hyperlink = f'<a href="{radar_chart_filename}">{radar_chart_filename}</a>'


                radar_chart_list.append(radar_chart_filename)



                
                if write_path==1:
                    usn_data.append(radar_chart_hyperlink)
                    usn_data[-1] = radar_chart_hyperlink
                csv_writer.writerow(usn_data)

                print("data saved successfully, heading on to next usn")
                # driver.refresh()
                firstnum = firstnum+1
            else:
                # driver.refresh()
                firstnum = firstnum+1  # increment in enrollment number
                print("enrollment number is not found")

            if firstnum-1 ==lastusn:
                print("SUCCESSFULLY FETCHED ALL RESULTS")
                break
    
        convert_radar_charts_to_pdf(radar_chart_list)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"PDF Generated Successfully with time: {execution_time:.4f} seconds")

  

# FUNCTION TO CALCULATE SGPA AND AUTOMATE TO TAKE THE VALUES OF CREDITS  
def calculate_sgpa(data, grade_points, subject_credits):
    red=0
    total_credits = 0
    total_credit_points = 0
    subject_code_credits = {}  # Create a dictionary to store subject code credits

    for row in data:
        if row:
            subject_code, _, _, _, _, result = row
            credit = subject_credits.get(subject_code)  # Try to get credits from the JSON file

            # If credits are not defined in the JSON file, ask the user for input
            if credit is None:
                if red==0:
                    messagebox.showwarning("Warning", "New Subject Codes found! ")
                    red=1
                credit = simpledialog.askstring("Input",f"Enter credits for subject code {subject_code}: ")
                subject_credits[subject_code] = credit  # Store credits in the JSON file
                with open("/home/picchai/result_automation_system/config.json", "w") as config_file:
                    json.dump(config, config_file, indent=4)  # Update JSON file

            credit = int(credit)  # Convert to integer
            grade_point = grade_points.get(result, 0)
            total_credits += credit
            total_credit_points += credit * grade_point
            subject_code_credits[subject_code] = credit  # Store credits in the subject_code_credits dictionary

    if total_credits > 0:
        sgpa = total_credit_points / total_credits
    else:
        sgpa = 0

    if print_v == 1:
        print("Total Credits:", total_credits)
        print("Total Credit Points:", total_credit_points)
        print("SGPA IS:", sgpa)
        print("Subject Code Credits:", subject_code_credits)

    print("SGPA calculated successfully")

    return sgpa, total_credit_points

# FUNCTION TO SHORTEN SUBJECT NAMES AND GIVE THE SHORT SUBJECT NAMES
def shorten_name(data):
    subject_names = []
    for row in data:
        if row:
            _, name,_,_,_,_,=row
            words = name.split()
            # Initialize an empty string to store the shortened name
            shortw = ""
            # If there is only one word, take the first 3 letters
            if len(words) == 1:
                shortw = words[0][:3]
                shortw = shortw.upper()
            elif len(words) == 2:
                shortw = words[0][0] + words[1][0] + words[1][-1]
                shortw = shortw.upper()
            else:
                # Take the first letter of each word and join them
                shortw = ''.join(word[0] for word in words)
                shortw = shortw.upper()
            subject_names.append(shortw)
    if print_v==1:
        print(subject_names)
    return subject_names

# Function to convert a list of PNG images to a PDF
def convert_radar_charts_to_pdf(radar_chart_list):
    # Define custom page dimensions in pixels (640x480)
    page_width = 640  # 640 pixels
    page_height = 480  # 480 pixels
    write_path=config["write_radarpath"]

    # Create a custom-sized PDF with portrait orientation
    pdf = FPDF(orientation='P', unit='pt', format=(page_width, page_height))

    watermark_image_path = config["watermark_image"]

    for radar_chart_filename in radar_chart_list:
        pdf.add_page()  # Add a new page for each image
        pdf.image(radar_chart_filename, x=0, y=0, w=page_width, h=page_height, type='PNG', link=radar_chart_filename)  # Specify type and link to maintain image quality
        pdf.image(watermark_image_path, x=page_width - 50, y=page_height - 50, w=40, h=30, type='PNG')
        if write_path == 0:
            os.remove(radar_chart_filename)

    # Specify the PDF output path
    pdf_output_path = config["pdf_path"]
    pdf.output(pdf_output_path)


# main function
if __name__ == "__main__":
    main()