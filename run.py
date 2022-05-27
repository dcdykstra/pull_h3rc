from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains 
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import unittest
import time

from loginPage import LoginPage
from navigate import Navigate
from cpt_report import CPTs_Report_Page
from stage import Stage
from encounter_provider_report import EP_DetReport_Page

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

    def test_cpt_valid(self): 
        driver = self.driver
        wait = self.wait
        driver.get("https://service.emedpractice.com/index.aspx")

        login = LoginPage(driver, wait)
        login.enter_username("test")
        login.enter_password("pass") 
        login.click_login()

        nav = Navigate(driver, wait)
        nav.nav_reports()
        nav.load_report("cpt_bills_reportV2")

        cpt = CPTs_Report_Page(driver, wait)
        cpt.enter_cpt_code("99214,99123")
        
        stage = Stage(driver, wait)
        stage.stage_dr("YTD", "R", "01-01-2022", "05-23-2022", 28)
        time.sleep(5)

    @classmethod
    def tearDownClass(cls):
        cls.driver.close()
        cls.driver.quit()
        print("Driver Closed")

if __name__ == '__main__':
    unittest.main()