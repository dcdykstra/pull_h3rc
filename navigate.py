from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import re
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

class Navigate():
    def __init__(self, driver, wait) -> None:
        self.driver = driver
        self.wait = wait

    def reset_iframe(self):
        self.driver.switch_to.default_content()
    
    def make_soup(self):
        return BeautifulSoup(self.driver.page_source, "html.parser")

    # Navigates to the reports page
    def nav_reports(self): 
        self.reports_menu = self.wait.until(EC.presence_of_element_located((By.XPATH, '//a[contains(@href, "tabname=Reports")]')))
        self.reports_menu.click()

    # Loads a specific report when on the reports page
    def load_report(self, report_href):
        self.reset_iframe()
        content_iframe = self.wait.until(EC.presence_of_element_located((By.ID, 'contentframe')))
        self.driver.switch_to.frame(content_iframe)
        report = self.wait.until(EC.presence_of_element_located((By.XPATH, f'//a[contains(@href, "{report_href}")]')))
        self.driver.execute_script("arguments[0].click();", report)
        report_iframe = self.wait.until(EC.presence_of_element_located((By.ID, 'ReportMasterFrame')))
        self.driver.switch_to.frame(report_iframe)

    ## For Searching and Pulling Patient Demographics

    # Navigates to the patient search page
    def nav_patients(self): 
        self.reset_iframe()
        nav_menu = self.wait.until(EC.presence_of_element_located((By.XPATH, '//a[contains(@href, "tabname=Patients")]')))
        nav_menu.click()
        content_iframe = self.wait.until(EC.presence_of_element_located((By.ID, 'contentframe')))
        self.driver.switch_to.frame(content_iframe)

    # Creates a dictionary of keys to search by in the patient search page
    def patients_search_dict(self): 
        self.nav_patients()
        soup = self.make_soup()
        inputs = soup.find_all("input", class_ = re.compile("text ui-widget-content ui-corner-all"))
        keys = []
        vals = []
        for i in inputs:
            vals.append(i.get("id"))
        spans = soup.find_all("span", id = re.compile("_ctl0_ContentPlaceHolder1_lbl"), style = "color:Black;font-family:verdana;font-size:8pt;font-weight:normal;text-decoration:none;")
        for i in spans:
            keys.append(i.text)
        return dict(zip(keys, vals))
    
    # Searches for a patient when on the patient search page with a key and value
    def search_patients(self, key, value): 
        query_select = self.wait.until(EC.element_to_be_clickable((By.ID, self.patients_search_dict().get(key))))
        query_select.clear()
        query_select.click()
        query_select.send_keys(value, Keys.RETURN)
    
    # Opens a patient file based on a chart number
    def open_patient_file(self, chart):
        self.reset_iframe()
        self.nav_patients()
        self.search_patients("Chart#", chart)
        pf = self.driver.find_element(By.ID, '_ctl0_ContentPlaceHolder1_gvCurrentPatient__ctl2_hlSelect')
        pf.click()
        
        demo = self.driver.find_element(By.XPATH, '//a[contains(@href, "PatientDetails")]')
        demo.click()