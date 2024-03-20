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
    chromedriver_path = os.getenv('MY_PATH_TO_CHROMEDRIVER')
    service = Service(executable_path=chromedriver_path)

    # Initialize the Chrome WebDriver with the specified service and options
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        print("Attempting to navigate to the Moodle login page...")
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
        print("Login successful. Navigating to the attendance page...")
        print("Navigating to current day's attendance...")
        # Navigate to the Moodle attendance page
        driver.get("https://moodle.becode.org/mod/attendance/view.php?id=311")
        time.sleep(2)

            # Find all elements with the "attbtn" class
        att_buttons = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".attbtn a"))
        )

        # Iterate over the buttons and click the one with the text "Days"
        for button in att_buttons:
            if "Days" in button.text:
                button.click()
                break


        # Get the current time to determine if it's time to check in or out
        now = datetime.now()
        current_hour_minute = now.hour * 100 + now.minute

        # Adjusting for specific check-in and check-out times as you wish
        check_in_time = [848, 1329]  # 09:00 AM and 1:30 PM
        check_out_time = [1230, 1655]  # 12:33 PM and 17:00 PM
        
        print("Determining if it's time to check in or out...")
            # Check if it's time to check in and if so, click the check-in button
        if any(check_time <= current_hour_minute <= check_time + 8 for check_time in check_in_time):
            # Logic to find and click the "Check in" button
            print("Time to check in.")
            try:
                check_in_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Check in')]"))
                )
                check_in_button.click()
                print("Check-in button clicked.")
            except Exception as e:
                print(f"An error occurred while clicking the 'Check in' button: {e}")
                
            try:
                # Wait for the dropdown to be visible
                WebDriverWait(driver, 10).until(
                     EC.visibility_of_element_located((By.NAME, "location"))
                  )

                # Determine the current day of the week
                current_day = datetime.now().weekday()
                
                # Select the dropdown
                location_select = Select(driver.find_element(By.NAME, "location"))

                # Logic to select "On campus" or "At home" based on the day of the week
                location_value = ""
                if current_day in [0, 1]:  # If it's Monday (0) or Tuesday (1)
                    location_value = "oncampus"
                else:  # For other days
                    location_value = "athome"
                
                location_select.select_by_value(location_value)
                print(f"Location selected: {location_value.capitalize()}")

                # Click the submit button to complete the action
                driver.find_element(By.NAME, "submitbutton").click()
                print("Form submitted successfully.")
            except Exception as e:
                print(f"An error occurred while selecting location and submitting the form: {e}")

        # Check if it's time to check out and if so, click the check-out button
        elif any(check_time <= current_hour_minute <= check_time + 8 for check_time in check_out_time):
            # Similar logic for "Check out"
            print("Time to check out.")

            check_out_buttons = driver.find_elements(
                By.CSS_SELECTOR, "a.btn[href*='checkout']")
            for button in check_out_buttons:
                if button.is_displayed():
                    button.click()
                    break
            print("Check-out completed.")
        else:
                    print("It's neither time to check in nor check out.")

    except Exception as e:
            print(f"An error occurred: {e}")

    finally:
        print("Closing the browser...")
        driver.quit()


if __name__ == "__main__":
    moodle_attendance()
