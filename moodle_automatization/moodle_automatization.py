from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime
from dotenv import load_dotenv
import os

# Load environment variables from the .env file in the same directory
load_dotenv()

def moodle_attendance():
    # Set Chrome options for the WebDriver
    chrome_options = webdriver.ChromeOptions()
    
    # Define the service using ChromeDriver executable path. Change 'MY_PATH_TO_CHROMEDRIVER' to your actual path in the env file
    service = Service(executable_path='MY_PATH_TO_CHROMEDRIVER')
    
    # Initialize the Chrome WebDriver with the specified service and options
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        # Navigate to Moodle login page
        driver.get("https://moodle.becode.org/login/index.php")
        # Wait for the page elements to load
        time.sleep(2)
         # Enter username and password from environment variables and click login
        driver.find_element(By.NAME, "username").send_keys(
            os.getenv('MOODLE_USERNAME'))
        driver.find_element(By.NAME, "password").send_keys(
            os.getenv('MOODLE_PASSWORD'))
        driver.find_element(By.ID, "loginbtn").click()
        # Wait for redirect after login
        time.sleep(2)

        # Navigate to the Moodle attendance page
        driver.get("https://moodle.becode.org/mod/attendance/view.php?id=311")
        time.sleep(2)

        # Find and click on the "Days" button to view the attendance for the current day
        days_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, ".attbtn > a[href*='&view=2']"))
        )
        days_button.click()

        # Get the current time to determine if it's time to check in or out
        now = datetime.now()
        current_hour_minute = now.hour * 100 + now.minute
        day_of_week = now.weekday()

        # Adjusting for specific check-in and check-out times as you wish
        check_in_time = [850, 1326]  # 8:50 AM and 1:26 PM
        check_out_time = [1233, 1658]  # 12:33 PM and 16:58 PM


        # Check if it's time to check in and if so, click the check-in button
        if any(check_time <= current_hour_minute <= check_time + 8 for check_time in check_in_time):
            # Logic to find and click the "Check in" button
            check_in_buttons = driver.find_elements(
                By.CSS_SELECTOR, "a.btn[href*='checkin']")
            for button in check_in_buttons:
                if button.is_displayed():
                    button.click()
                    # Wait for the "select location" dropdown to be present after clicking "Check in"
                    WebDriverWait(driver, 10).until(
                        EC.visibility_of_element_located((By.NAME, "location"))
                    )
                    break

            # After the dropdown is visible, select "On campus" or "At home" and submit
            location_select = Select(driver.find_element(By.NAME, "location"))
            if day_of_week in [0, 1]:  # Monday or Tuesday for "On campus"
                location_select.select_by_value("oncampus")
            else:  # Other days for "At home"
                location_select.select_by_value("athome")
            # Click the submit button to complete the check-in
            driver.find_element(By.NAME, "submitbutton").click()

        # Check if it's time to check out and if so, click the check-out button
        elif any(check_time <= current_hour_minute <= check_time + 8 for check_time in check_out_time):
            # Similar logic for "Check out"
            check_out_buttons = driver.find_elements(
                By.CSS_SELECTOR, "a.btn[href*='checkout']")
            for button in check_out_buttons:
                if button.is_displayed():
                    button.click()
                    break

    finally:
        driver.quit()


if __name__ == "__main__":
    moodle_attendance()
