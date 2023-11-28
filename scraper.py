
import os

import glob

import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


DOWNLOAD_PATH = ""
EXECUTABLE_PATH = ""
EMAIL = ""
PWD = ""
ASSIGNMENT_NAME = ""
COURSE_NUMBER = ""

service = Service(executable_path=EXECUTABLE_PATH)
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")

os.makedirs(DOWNLOAD_PATH, exist_ok=True)

prefs = {
    "download.default_directory" : DOWNLOAD_PATH,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "plugins.always_open_pdf_externally": True
}


options.add_experimental_option("prefs",prefs)

driver = webdriver.Chrome(service=service, options=options)


driver.get("https://www.gradescope.com/")


login = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//button[@type='button']")))


login.click()


WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "session_email"))).send_keys(EMAIL)


WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "session_password"))).send_keys(PWD)


login_button = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//input[@name='commit']")))


login_button.click() 


class_button = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, f"//a[@href='/courses/{COURSE_NUMBER}']")))


class_button.click()


assignment_button = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.LINK_TEXT, ASSIGNMENT_NAME)))


assignment_button.click()


manage_submissions = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//div[text()='Manage Submissions']")))


manage_submissions.click()


submission_url = driver.current_url


total_pages = int(driver.find_elements(By.CLASS_NAME, "paginate_button")[-2].text)


for i in range(total_pages): 
    table = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "table--primaryLink")))

    submissions = [x.find_element(By.TAG_NAME, "a").get_attribute("href") for x in driver.find_elements(By.CLASS_NAME, "table--primaryLink")]

    for submission in submissions:
        driver.get(submission)

        student_name = driver.find_element(By.CLASS_NAME, "submissionOutlineHeader--groupMember").text.replace(" ", "")

        download_button = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//span[text()='Download Graded Copy']")))

        previous_length = len(glob.glob(os.path.join(DOWNLOAD_PATH, "*.pdf")))

        download_button.click()

        wait = 0

        while previous_length == len(glob.glob(os.path.join(DOWNLOAD_PATH, "*.pdf"))) and wait < 30:
            time.sleep(2)
            wait+=1

        list_of_files = glob.glob(os.path.join(DOWNLOAD_PATH, "*.pdf"))

        latest_file = max(list_of_files, key=os.path.getctime)

        new_file_name = latest_file.replace(os.path.basename(latest_file), f"HW6_{student_name}.pdf")

        os.rename(latest_file, new_file_name)
    
    driver.get(submission_url)

    for j in range(i+1):

        next_button = driver.find_elements(By.CLASS_NAME, "paginate_button")[-1]

        next_button.click()








