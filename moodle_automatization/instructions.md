# Moodle Attendance Automation

This project automates the process of checking in and out on the Moodle platform, tailored specifically for BeCode's attendance system. It uses Python and Selenium to interact with the web pages, automating daily attendance tasks based on the time of day and day of the week.

## Prerequisites

- Python 3.x
- Selenium WebDriver
- ChromeDriver compatible with your version of Google Chrome
- Google Chrome Browser

# Moodle Attendance Automation

This project automates the process of checking in and out on the Moodle platform, tailored specifically for BeCode's attendance system. It uses Python and Selenium to interact with web pages, automating daily attendance tasks based on the time of day and day of the week.

## Prerequisites

- Python 3.x
- Selenium WebDriver
- ChromeDriver compatible with your version of Google Chrome
- Google Chrome Browser

## Setup Instructions

1. **Install Python 3.x**:

   - Download and install from [python.org](https://www.python.org/downloads/).

2. **Install Selenium**:

   - Run `pip install selenium` in your terminal or command prompt to install the Selenium package.

3. **Download ChromeDriver**:

   - Go to the [ChromeDriver downloads page](https://sites.google.com/chromium.org/driver/) and download the version that matches your Google Chrome browser.
   - Extract and save `chromedriver.exe` to a known location on your system.

4. **Clone the Repository**:

   - Clone this repository to your local machine using `git clone <repository-url>`.

5. **Create an Environment Variables File**:

   - In the project directory, create a new file named `.env`.
   - Open `.env` file in a text editor and add the following lines:

     ```
     MOODLE_USERNAME=your_username
     MOODLE_PASSWORD=your_password
     MY_PATH_TO_CHROMEDRIVER=your_path_to_chromedriver
     ```

   - Replace `your_username` and `your_password` with your actual Moodle credentials.

6. **Update the Script**:
   - Open `moodle_attendance.py` in a text editor.
   - Update the `executable_path` in the `Service` object with the path to your `chromedriver.exe`.
   - Replace `"YOUR_USERNAME"` and `"YOUR_PASSWORD"` with your actual Moodle login credentials.

## Running the Script Manually

To run the script manually:

1. Open a terminal or command prompt.
2. Navigate to the directory where `moodle_attendance.py` is located.
3. Execute the script by running:

   ```shell
   python moodle_attendance.py
   ```

4. The script will automatically open a Chrome browser window, log into Moodle with the credentials from your `.env` file, navigate to the attendance page, and perform the check-in or check-out operation based on the current time and day.

### It's important not to upload your .env file to version control or share it with others as it contains sensitive information

#### Ensure that your .env file is listed in your .gitignore if using git to prevent it from being committed

## Automation

For automated execution, we will be using scheduling tools like cron jobs on Linux/Mac or Task Scheduler on Windows. Set up the tool to run the script at times just before your check-in and check-out times.

### Windows

Use Task Scheduler:

1. **Open Task Scheduler**: Press `Windows+R`, type `taskschd.msc`, and press Enter.
2. **Create a New Task**: Go to the Action menu and select "Create Basic Task..." or "Create Task..." for more configurations.
3. **Define the Trigger**: Follow the wizard to name your task and choose its trigger. Select the frequency and exact time for the script to run.
4. **Set the Action**: Choose "Start a program" as the action. For the program/script, input the path to your Python executable. In "Add arguments", input the path to your script, e.g., `D:\path\to\your\moodle_attendance.py`.
5. **Finish Setup**: Complete the wizard. You can test the task by right-clicking on it in the Task Scheduler Library and selecting "Run".

### macOS

Using `cron`:

1. **Open Terminal**.
2. **Edit Crontab**: Type `crontab -e` to edit the cron jobs.
3. **Schedule Your Script**: Add a line in cron format, e.g., to run every day at 8 AM:

```shell
0 8 * * * /usr/bin/python3 /path/to/your/moodle_attendance.py
```

Replace `/usr/bin/python3` with the path to your Python executable, found using `which python3`. 4. **Save and Exit**: The cron job is now scheduled.

### Linux

Similar to macOS, using `cron`:

1. **Open Terminal**.
2. **Edit Crontab**: Type `crontab -e`.
3. **Add Your Script to the Schedule**: For example, to run at 9 AM daily:

```shell
0 9 * * * /usr/bin/python3 /path/to/your/moodle_attendance.py
```

Replace `/usr/bin/python3` with the path to your Python executable, found using `which python3`.

1. **Save and Exit**: Your script is now scheduled to run automatically.

### Notes

- Ensure the paths to Python and your script are absolute.
- On macOS and Linux, running scripts that require GUI interaction without a logged-in user environment might need adjustments, such as using Selenium in headless mode.
- Ensure your computer remains awake and logged in (if required) at the scheduled times. Adjust power settings as needed to prevent sleep mode.
