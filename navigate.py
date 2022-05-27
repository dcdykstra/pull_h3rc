from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

class Navigate():
    def __init__(self, driver, wait) -> None:
        self.driver = driver
        self.wait = wait

    def reset_iframe(self):
        self.driver.switch_to.default_content()

    def nav_reports(self): 
        self.reports_menu = self.wait.until(EC.presence_of_element_located((By.XPATH, '//a[contains(@href, "tabname=Reports")]')))
        self.reports_menu.click()

    def load_report(self, report_href):
        self.reset_iframe()
        content_iframe = self.wait.until(EC.presence_of_element_located((By.ID, 'contentframe')))
        self.driver.switch_to.frame(content_iframe)
        report = self.wait.until(EC.presence_of_element_located((By.XPATH, f'//a[contains(@href, "{report_href}")]')))
        self.driver.execute_script("arguments[0].click();", report)
        report_iframe = self.wait.until(EC.presence_of_element_located((By.ID, 'ReportMasterFrame')))
        self.driver.switch_to.frame(report_iframe)