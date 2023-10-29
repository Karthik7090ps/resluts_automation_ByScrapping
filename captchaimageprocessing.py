import cv2
import numpy as np
import numpy as np
import matplotlib.pyplot as plt

# Load the image
img = cv2.imread('/home/picchai/Downloads/test captcha/3.jpeg')

#############################FUNCTION TO PROCESS CAPTCHA IMAGE ##############################
def image_proc(img):
    gry = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    (h, w) = gry.shape[:2]
    gry = cv2.resize(gry, (w*2, h*2))
    cls = cv2.morphologyEx(gry, cv2.MORPH_CLOSE, None)
    thr = cv2.threshold(cls, 100, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]



    # Display the original and brightened images
    cv2.imshow('Original Image', img)
    cv2.imshow('Brightened Image', thr)

    # Wait for a key press and then close the windows
    cv2.waitKey(0)
    cv2.destroyAllWindows()

############################# FUNCTION TO DOWNLOAD THE CAPTCHA ######################################
def download_image(url, image_name):
    file_name = image_name
    res = requests.get(url, stream=True)
    if res.status_code == 200:
        with open(file_name, 'wb') as f:
            shutil.copyfileobj(res.raw, f)
        return True
    else:
        pass


############################ FUNCTION TO FIND URL OF THE CAPTCHA FOR CHANGING ID OF CAPTCHA ###########
def find_src(s):
    captcha_numbers = re.findall(r'/captcha/(\d+)"', s)

    # The last element in the list is the last captcha-related number
    if captcha_numbers:
        link = captcha_numbers[-1]
        print("Last captcha number:", link)
        return link
    else:
        print("No captcha numbers found in the HTML.")


############################## FUNCTION TO SHORTEN NAME #############################
def shorten_name(name):
    # Split the name into words
    words = name.split()

    # Initialize an empty string to store the shortw name
    shortw = ""

    # If there is only one word, take the first 3 letters
    if len(words) == 1:
        shortw = words[0][:3]
    else:
        # Take the first letter of each word and join them
        shortw = ''.join(word[0] for word in words)
        shortw = shortw.upper()

    return shortw

############################## RADAR CHART FUNCTION ################################
# import numpy as np
# import matplotlib.pyplot as plt

# Sample data - replace with your actual data
usn = "1BM22EC001"
grades = ["B", "A", "B+", "C", "A", "A+", "B", "B+", "A", "O", "C", "D"]

# Define the short names of subjects (replace with your subject names)
subject_names = ["Math", "Physics", "Chemistry", "Biology", "History", "Geography", "English", "Art", "Music", "PE", "Computer", "Ethics"]

# Create a radar chart
def create_radar_chart(usn, grades, sub):
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
        ax.plot([0, angle], [0, max(values)], color='k', linewidth=1, linestyle='--')

    # Draw the border of the radar chart by plotting a polygon
    border = plt.Polygon(np.column_stack([angles, values]), edgecolor='k', linewidth=2, closed=True, fill=False)
    ax.add_patch(border)

    # Plot the radar chart
    ax.fill(angles, values, 'b', alpha=0.1)
    ax.set_yticklabels([])

    # Set the radial grid lines
    ax.set_xticks(angles)
    ax.set_xticklabels(labels)

    ax.set_title(usn)

    # Plot grades with points
    for angle, value, grade in zip(angles, values, filtered_grades):
        x, y = np.cos(angle), np.sin(angle)
        ax.plot(angle, value, 'ro', markersize=8)  # Plot the grade point
        ax.text(angle, value, grade, ha='center', va='bottom')

    radar_chart_filename = f'{usn}_radar_chart.png'
    plt.savefig(radar_chart_filename)  # Removed bbox_inches='tight'

    plt.close()

    return radar_chart_filename

