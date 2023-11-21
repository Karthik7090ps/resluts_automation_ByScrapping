
# Automated Student Result Analysis Tool

This tool automates the process of extracting and analyzing student results from a web portal. It is designed to work with specific university results web pages and generate radar charts for individual students based on their academic performance.

**Note:** This tool is provided for educational purposes only and should be used responsibly and in compliance with the terms of service of the target website.

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [How It Works](#how-it-works)
- [Contributing](#contributing)
- [License](#license)

## Features

- Web scraping of student results.
- Calculation of SGPA (Semester Grade Point Average) based on grades and credits.
- Generation of radar charts to visualize academic performance.
- CSV output with student details and results.
- Option to save radar charts in PDF format.

## Requirements

- Python 3.x
- Selenium
- OpenCV
- pytesseract
- pandas
- numpy
- matplotlib
- tkinter
- Pillow (PIL)
- fpdf

You can install the required Python packages using pip:

```bash
pip install selenium opencv-python-headless pytesseract pandas numpy matplotlib pillow fpdf
```

Additionally, you need the [Chrome WebDriver](https://sites.google.com/a/chromium.org/chromedriver/downloads) installed and accessible in your system's PATH.

## Installation

1. Clone the repository to your local machine:

```bash
git clone https://github.com/your-username/automated-result-analysis-tool.git
cd automated-result-analysis-tool
```

2. Download and install the [Chrome WebDriver](https://sites.google.com/a/chromium.org/chromedriver/downloads).

3. Update the `config.json` file to configure the tool according to your requirements. (See [Configuration](#configuration))

## Usage

To use the Automated Student Result Analysis Tool, run the following command:

```bash
python result_analysis.py
```

Follow the on-screen prompts to enter the necessary information and proceed with web scraping and analysis.

## Configuration

The `config.json` file is used to configure the tool. Here's an explanation of the configuration options:

- `print_debug_data`: Set to 0 to suppress debug messages, 1 to enable them.
- `screen_show`: Set to 1 to display the browser window during web scraping, 0 for headless mode.
- `auto`: Set to 1 to use automatic configuration, 0 for manual configuration.
- `firstnum`: Starting number of the student's USN.
- `lastusn`: Last number of the student's USN.
- `usn_num`: The branch and semester code in the USN (e.g., "1bm22ec" for a specific branch).
- `status`: Set to "y" for an infinite loop of solving captchas, "n" for a limited number of attempts.
- `write_radarpath`: Set to 1 to include radar chart filenames in the CSV, 0 to exclude them.
- `developer_mode`: Set to 1 for developer mode, which shows additional pop-up messages.
- `result_link`: URL of the result page to scrape.
- `captcha_image`: Path to save captcha images.
- `radar_save`: Path to save radar chart images with a placeholder `{{usn}}`.
- `pdf_intake`: Directory path where radar charts are saved before converting to a PDF.
- `csv_path`: Path to save the CSV file with student results.
- `pdf_path`: Path to save the final PDF containing radar charts.
- `grade_points`: Mapping of grades to grade points.
- `subject_credits`: Mapping of subject codes to their credit values.

## How It Works

The tool uses Selenium to automate the process of filling in student information and scraping result data from the target web portal. It then calculates the SGPA based on grades and credits, generates radar charts to visualize academic performance, and stores the data in a CSV file.

## Contributing

Contributions to this project are welcome. If you have suggestions or find any issues, please feel free to submit a pull request or open an issue.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
```

Make sure to replace `"https://github.com/your-username/automated-result-analysis-tool.git"` with the actual URL of your GitHub repository.

This README file provides users with clear instructions on how to install, configure, and use your tool. Users will be able to understand the purpose of your code, how it works, and how to contribute to the project.