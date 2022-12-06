
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.options import Options
import json
from time import sleep

from coursework_extensions.addresses import DLO_DIR


class Campus:
    def __init__(self, login_file):
        options = Options()
        options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'
        self.driver = webdriver.Firefox(options=options)
        self.driver.get('https://campus.nottingham.ac.uk/psp/csprd/?cmd=login')
        self.driver.maximize_window()
        with open(login_file) as f:
            login_details = json.loads(f.read())
        self.login(login_details['username'], login_details['password'])


    def login(self, username, password):
        username_box = self.driver.find_element_by_id('userid')
        password_box = self.driver.find_element_by_id('pwd')
        sign_in = self.driver.find_element_by_class_name('ps-button')

        username_box.send_keys(username)
        password_box.send_keys(password)
        sign_in.click()

    def _campus_wait_for_load(self, selector, by='id'):
        not_found=True
        while not_found:
            try:
                if by == 'id':
                    self.driver.find_element_by_id(selector).click()
                elif by == 'text':
                    self.driver.find_element_by_link_text(selector).click()
                not_found = False
            except:
                sleep(1)


    def download_student_records(self, timeout=20):
        #Open mystudents
        self._campus_wait_for_load('win0groupletPTNUI_LAND_REC_GROUPLET$0')
        #Open Disability associations
        self._campus_wait_for_load("UN_ACAD_STD_H_DESCR60$span$1")
        #Select all checkbox
        self._campus_wait_for_load("UN_ACAD_STD_WRK_UN_SELECT_ALL$IMG")
        #click download arrow
        self._campus_wait_for_load("UN_ACAD_STD_WRK_UN_EXPORT_PB$IMG")
        #click export on popup
        sleep(5)

        export_form = self.driver.find_element_by_id('win0divUN_ACAD_STD_WRK_UN_EXPORT_PB')
        # create action chain object
        # perform the operation
        element = self.driver.find_element_by_xpath('//*[@id="UN_AWC_WRK_UN_EXPORT_PB"]')
        self.driver.execute_script("arguments[0].click();", element)


















if __name__ == '__main__':
    campus = Campus(DLO_DIR + 'login.json')
    campus.download_student_records()