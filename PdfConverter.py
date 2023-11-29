import os
import json
from fpdf import FPDF
import pygame
from natsort import natsorted

with open("/home/picchai/Documents/GItHub/resluts_automation_ByScrapping/config.json", "r") as config_file:
    config = json.load(config_file)

directory_path = config["pdf_intake"]
start_id = config["usn_num"] + config["spdfrange"]
end_id = config["usn_num"] + config["epdfrange"]

def convert_student_range_to_pdf(start_usn, end_usn, folder_path):
    # Collect all PNG files in the specified folder
    png_files = [f for f in os.listdir(folder_path) if f.endswith('.png')]

    # Filter PNG files based on the provided range
    filtered_png_files = [os.path.join(folder_path, file) for file in png_files if start_usn <= file.split('_')[0] <= end_usn]


    # Use the existing conversion code with the filtered images
    convert_radar_charts_to_pdf(filtered_png_files)
    print("Successfully Generated the PDF1 File")
    play_sound()

def convert_radar_charts_to_pdf(radar_chart_list):
    # Sort the list based on natural alphanumeric order
    sorted_files = natsorted(radar_chart_list)

    # Define custom page dimensions in pixels (640x480)
    page_width = 640  # 640 pixels
    page_height = 480  # 480 pixels

    write_path = config["write_radarpath"]

    # Create a custom-sized PDF with portrait orientation
    pdf = FPDF(orientation='P', unit='pt', format=(page_width, page_height))

    watermark_image_path = config["watermark_image"]

    for radar_chart_filename in sorted_files:
        pdf.add_page()  # Add a new page for each image
        pdf.image(radar_chart_filename, x=0, y=0, w=page_width, h=page_height, type='PNG', link=radar_chart_filename)  # Specify type and link to maintain image quality
        pdf.image(watermark_image_path, x=page_width - 50, y=page_height - 50, w=40, h=30, type='PNG')
        os.remove(radar_chart_filename)

    # Specify the PDF output path
    pdf_output_path = config["pdf_path"]
    pdf.output(pdf_output_path)

def play_sound():
    pygame.init()
    pygame.mixer.music.load('/home/picchai/Documents/GItHub/resluts_automation_ByScrapping/complete.wav')
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

convert_student_range_to_pdf(start_id, end_id, directory_path)
