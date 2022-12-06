
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
from time import sleep



class campus:
    def __init__(self, login_file):
        self.driver = webdriver.Chrome()
        self.driver.get('https://campus.nottingham.ac.uk/psp/csprd/?cmd=login')
        login_details = json.load(login_file)
        login(login_details['username'], login_details['password'])


    def login(username, password):




if __name__ == '__main__':
    create_driver()