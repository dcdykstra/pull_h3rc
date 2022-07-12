from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd
from unidecode import unidecode
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class CPTs_Report_Page():
    def __init__(self, driver, wait) -> None:
        self.driver = driver
        self.wait = wait
        self.cpt_txtbox_id = '_ctl0_ContentPlaceHolder1_txtcpt'

    def make_soup(self):
        return BeautifulSoup(self.driver.page_source, "html.parser")
    
    def enter_cpt_code(self, cpt_code):
        self.driver.find_element(By.ID, self.cpt_txtbox_id).clear()
        self.driver.find_element(By.ID, self.cpt_txtbox_id).send_keys(cpt_code)

    def pull(self, savefile):
        try:
            table = self.wait.until(EC.presence_of_element_located((By.ID, "_ctl0_ContentPlaceHolder1_gvreport")))
            soup = self.make_soup()
            table = soup.find_all("table", id = "_ctl0_ContentPlaceHolder1_gvreport")
            body = table[0].find("tbody")

            head = table[0].find("thead").find_all("th")
            cpt_headers = [unidecode(i.text.strip()) for i in head]

            temp = []
            for i in body.find_all("tr"):
                temp.append([unidecode(j.text) for j in i.find_all("td")])

            df = pd.DataFrame(temp, columns = cpt_headers)
            df["Bill#"] = df["Bill#"].apply(lambda x: x.strip("\n"))
            df.drop(df.tail(1).index, inplace=True)
            df.to_csv(savefile)
            
        except TimeoutException:
            print("No Table")