from selenium import webdriver
import json
from typing import List
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Firefox()

driver.get("https://services.gst.gov.in/services/login/")

def navigate():
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '/html/body/adhr-table/div/div/div/div[2]/a[2]')))
    initial_banner = driver.find_element
    driver.find_element(By.XPATH, '/html/body/div[1]/ng-include[2]/nav/div/div/ul/li[2]/ul/li[4]/div/ul/li[1]/a').click()

    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[2]/div/div[2]/div[2]/form/div/div[1]/select')))
    
    financial_year_select_element = Select(driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div/div[2]/div[2]/form/div/div[1]/select"))
    financial_year_select_element.select_by_visible_text('2023-24')
    time.sleep(0.5)
    quarter_select_element = Select(driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div/div[2]/div[2]/form/div/div[2]/select"))
    quarter_select_element.select_by_visible_text('Quarter 4 (Jan - Mar)')
    time.sleep(0.5)
    period_select_element = Select(driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div/div[2]/div[2]/form/div/div[3]/select"))
    period_select_element.select_by_visible_text('January')
    time.sleep(0.5)
    driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/div/div[2]/div[2]/form/div/div[4]/button').click()

def login():
    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "username")))
    username = driver.find_element(By.ID, 'username')
    password = driver.find_element(By.ID, 'user_pass')
    username.send_keys('Saha_2255')
    password.send_keys('Sahayi#2024')
    capcha = driver.find_element(By.ID, 'captcha')
    capcha_data = input('Enter the capcha data: ')
    capcha.send_keys(capcha_data)
    driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/div/div[2]/div/div/div/div/div/form/div[6]/div/button').click()
   
    
if __name__ == "__main__":
    login() 
    navigate()