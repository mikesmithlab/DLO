
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.options import Options
import json
from time import sleep
import shutil
import os
import glob


import sys
# setting path
sys.path.append('..')
from addresses import DLO_DIR


class Campus:
    def __init__(self, login_file):
        #options = Options()
        #options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'
        self.driver = webdriver.Chrome()
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
        #Download the spreadsheet - settle in for a long wait!
        self.driver.get('https://campus.nottingham.ac.uk/psc/csprd/EMPLOYEE/SA/s/WEBLIB_UN_AWC.ISCRIPT1.FieldFormula.IScript_GetExcelFile?term=CURR&option=ALL')
        #Put file somewhere sensible
        print('Downloaded')
        self._move_downloaded_file()


    def _move_downloaded_file(self):
        not_found=True
        while not_found:
            try:
                #Moves downloaded file to DLO
                print(os.environ['USERPROFILE'] + 'Downloads/StudentExport*.xlsx')
                exported_file = glob.glob(os.environ['USERPROFILE'] + '/Downloads/StudentExport*.xlsx')
                shutil.move(exported_file[0], DLO_DIR + 'Campus/student_export.xlsx')
                not_found=False
                print('Moved')
            except:
                sleep(5)

    def close(self):
        self.driver.quit()


if __name__ == '__main__':
    campus = Campus(DLO_DIR + 'login.json')
    campus.download_student_records()
    campus.close()