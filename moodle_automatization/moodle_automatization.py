from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
import time
from datetime import datetime

def moodle_attendance():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--ignore-ssl-errors=yes')
    chrome_options.add_argument('--ignore-certificate-errors')

    service = Service(executable_path='D:/Programare/Python/moodle_automatization/chromedriver.exe')
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        driver.get("https://moodle.becode.org/login/index.php")
        time.sleep(2)
        driver.find_element(By.NAME, "username").send_keys("YOUR_USERNAME_HERE")
        driver.find_element(By.NAME, "password").send_keys("YOUR_PASSWORD_HERE")
        driver.find_element(By.ID, "loginbtn").click()
        time.sleep(2)

        driver.get("https://moodle.becode.org/mod/attendance/view.php?id=311")
        time.sleep(2)
        
        now = datetime.now()
        current_hour_minute = now.hour * 100 + now.minute
        day_of_week = now.weekday()

        # Adjusting for specific check-in and check-out times
        check_in_time = [856, 1326]  # Example: 8:56 AM and 1:26 PM
        check_out_time = [1234, 1704]  # Example: 12:34 PM and 5:04 PM

        if any(check_time <= current_hour_minute <= check_time + 8 for check_time in check_in_time):
            # Logic to find and click the "Check in" button
            # Example: Finding by href attribute if "Check in" is part of the URL
            check_in_buttons = driver.find_elements(By.CSS_SELECTOR, "a.btn[href*='checkin']")
            for button in check_in_buttons:
                if button.is_displayed():  # Making sure the button is visible
                    button.click()
                    break
        elif any(check_time <= current_hour_minute <= check_time + 8 for check_time in check_out_time):
            # Similar logic for "Check out"
            check_out_buttons = driver.find_elements(By.CSS_SELECTOR, "a.btn[href*='checkout']")
            for button in check_out_buttons:
                if button.is_displayed():
                    button.click()
                    break

        time.sleep(2)

        # Logic to select "On campus" or "At home" and submit
        if "select location" in driver.page_source.lower():
            location_select = Select(driver.find_element(By.NAME, "location"))
            if day_of_week in [0, 1]:  # Monday or Tuesday for "On campus"
                location_select.select_by_value("oncampus")
            else:  # Other days for "At home"
                location_select.select_by_value("athome")

            driver.find_element(By.NAME, "submitbutton").click()

    finally:
        driver.quit()

if __name__ == "__main__":
    moodle_attendance()
