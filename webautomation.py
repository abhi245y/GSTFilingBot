from selenium import webdriver
import json
from typing import List
import time
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()

driver.get("https://services.gst.gov.in/services/login/")
cookies_path = './cookies.json'

input('Enter After Login')

def add_cookies(cookies: List[dict]) -> None:
    """
    Adds cookies to the driver for session management.

    Args:
        cookies (List[dict]): List of cookie dictionaries.
    """
    for cookie in cookies:
        driver.add_cookie(cookie)
    driver.get("https://return.gst.gov.in/returns/auth/dashboard")
    time.sleep(2)
    submit_button = driver.find_element(By.CLASS_NAME, "submit_button")
    submit_button.click()

with open(cookies_path, "r") as f:
    cookies = json.load(f)
add_cookies(cookies)


# with open('./cookies.json', "w") as f:
#     f.write(json.dumps(driver.get_cookies(), indent=4))