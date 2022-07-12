from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd
from unidecode import unidecode
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import re
from datetime import datetime

class Patient_Demo_Page():
    def __init__(self, driver, wait) -> None:
        self.driver = driver
        self.wait = wait

    def make_soup(self):
        return BeautifulSoup(self.driver.page_source, "html.parser")

    # Pulls the patient data from a demographic data input table 
    # FOR A SINGLE PATIENT
    def pull_patient_data(self):
        soup = self.make_soup()
        txt_inp = soup.find_all("input", type = "text", id = re.compile("_ctl0_ContentPlaceHolder1"))
        opt_sel = soup.find_all("select", id = re.compile("_ctl0_ContentPlaceHolder1"))
        btn_inp = soup.find_all("input", type="radio")
        chk_inp = soup.find_all("input", type="checkbox")
        order = ["Ethnicity *", "Sex *", "Date Of Birth *", "Country*", "State *", 'Preferred Language', 
                "Preferred Contact", 'Ok to receive msgs', 'App.Reminder Contact', "Status", 'Marital Status *', 
                "How did you find us?", "Gender Identity", "Sexual Orientation",
                "Facility", 'Automatically update Demographics information for self insured', 'Automatically update Address information in insurance (other relations)']
        
        txt_dict = {}
        keys = []
        for i in txt_inp:
            txt_key = unidecode(i.parent.find_previous("span").text)
            if txt_key == "Date Of Birth *":
                dt = datetime.strptime(i.get("value"), "%m/%d/%Y")
                txt_dict[txt_key] = dt.year
            elif txt_key in order:
                txt_dict[txt_key] = i.get("value")

        opt_dict = {}
        for i in opt_sel:
            opt_key = unidecode(i.parent.find_previous("span").text)
            if opt_key in order:
                selected = i.findChild("option", selected="selected")
                if (selected == None) or (selected.text in [None, "--Select--", "-Select-"]):
                    opt_dict[opt_key] = None    
                else:
                    opt_dict[opt_key] = selected.text

        btn_dict = {}
        for i in btn_inp:
            btn_key = unidecode(i.find_previous("span").text)
            if i.get("checked") == "checked":
                if i.get("name") == "_ctl0:ContentPlaceHolder1:Sex":
                    btn_dict["Sex *"] = btn_key

        race_dict = {}
        chk_dict = {}
        for i in chk_inp:
            if i.get("checked") == "checked":  
                if i.get('title') != None:
                    race_dict[i.get("title")] = 1
                else:
                    chk_dict[unidecode(i.nextSibling.text)] = 1
            else:
                if i.get('title') != None:
                    race_dict[i.get("title")] = 0
                else:
                    chk_dict[unidecode(i.nextSibling.text)] = 0
                    
        order = order + list(race_dict.keys())
        
        final_dict = {**txt_dict,**race_dict,**chk_dict,**btn_dict,**opt_dict}
        
        return {k: final_dict[k] for k in order}
        