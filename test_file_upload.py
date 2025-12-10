import os

from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time

def test_uploads(driver):
    driver.get("https://the-internet.herokuapp.com/upload")
    upload_file = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "selenium-snapshot.png"))

    file_input = driver.find_element(By.CSS_SELECTOR, "input[type='file']")
    file_input.send_keys(upload_file)
    driver.find_element(By.ID, "file-submit").click()

    file_name_element = driver.find_element(By.ID, "uploaded-files")
    file_name = file_name_element.text

    assert file_name == "selenium-snapshot.png"

def main():

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install())
    )

    test_uploads(driver)


if __name__ == '__main__':
    main()
