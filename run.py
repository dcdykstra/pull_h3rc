from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains 
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import unittest
import time
import pandas as pd

from loginPage import LoginPage
from navigate import Navigate
from cpt_report import CPTs_Report_Page
from stage import Stage
from encounter_provider_report import EP_DetReport_Page
from patient_report import Patient_Demo_Page

class RunTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.prefs = {'profile.default_content_setting_values.automatic_downloads': 1}
        cls.options = webdriver.ChromeOptions()
        # cls.options.add_argument('--headless')
        cls.options.add_argument('--disable-dev-shm-usage')
        cls.options.add_argument('--ignore-certificate-errors')
        cls.options.add_argument('--ignore-ssl-errors')
        cls.options.add_experimental_option('excludeSwitches', ['enable-logging'])
        cls.options.add_experimental_option('prefs', cls.prefs)
        cls.driver = webdriver.Chrome(service = Service(ChromeDriverManager().install()), options=cls.options)
        cls.actions = ActionChains(cls.driver)
        cls.wait = WebDriverWait(cls.driver, 20)

    # EXAMPLE GET PATIENT DEMOGRPAHIC DATA FOR A LIST OF PATIENTS (CHART #)
    # def test_patient_demo(self):
    #     driver = self.driver
    #     wait = self.wait
    #     driver.get("https://service.emedpractice.com/index.aspx")

    #     cl = pd.read_csv("E:\dir1\h3rc\cpt_codes\data\merged.csv")
    #     cl = pd.unique(cl["Chart#"]).tolist()

    #     login = LoginPage(driver, wait)
    #     login.enter_username("")
    #     login.enter_password("") 
    #     login.click_login()
        
    #     stage = Stage(driver, wait)
    #     stage.stage_demo(cl)

    ## EXAMPLE SEARCH FOR CPT CODES FROM A DATE RANGE
    def test_cpt_valid(self): 
        driver = self.driver
        wait = self.wait
        driver.get("https://service.emedpractice.com/index.aspx")

        login = LoginPage(driver, wait)
        login.enter_username("")
        login.enter_password("") 
        login.click_login()

        nav = Navigate(driver, wait)
        nav.nav_reports()
        nav.load_report("cpt_bills_reportV2")

        cpt = CPTs_Report_Page(driver, wait)
        cpt.enter_cpt_code("99214,99123")
        
        stage = Stage(driver, wait)
        stage.stage_dr("0-10-2022", "05-29-2022", 28)
        time.sleep(5)
    
    ## EXAMPLE GET PROVIDER REPORT
    # def test_ep_valid(self):
    #     driver = self.driver
    #     wait = self.wait
    #     driver.get("https://service.emedpractice.com/index.aspx")

    #     login = LoginPage(driver, wait)
    #     login.enter_username("")
    #     login.enter_password("") 
    #     login.click_login()

    #     nav = Navigate(driver, wait)
    #     nav.nav_reports()
    #     nav.load_report("ProviderDetailedReportV1")

    #     ep = EP_DetReport_Page(driver, wait)
    #     ep.deselect_ep()
    #     ep.select_ep(["DR. CHRISTINA M.B. WANG, DNP, MPH, APRN-Rx, A", "Angela Gough, DO", "JOHN PAUL MOSES III, APRN, FNP-C"])

    #     stage = Stage(driver, wait)
    #     stage.stage_dr("01-01-2022", "03-06-2022", 28)
    #     stage.merge("E:\\dir1\\h3rc\\cpt_codes\\data\\merged.csv")
    #     time.sleep(10)


    @classmethod
    def tearDownClass(cls):
        cls.driver.close()
        cls.driver.quit()
        print("Driver Closed")

if __name__ == '__main__':
    unittest.main()