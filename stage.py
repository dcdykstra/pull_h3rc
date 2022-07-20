from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
import pandas as pd
import os
import glob

from cpt_report import CPTs_Report_Page
from patient_report import Patient_Demo_Page
from navigate import Navigate
from datetime import datetime
from datetime import timedelta

class Stage():
    def __init__(self, driver, wait) -> None:
        self.driver = driver
        self.wait = wait
        self.run_btn_id = '_ctl0_ContentPlaceHolder1_btnRunItNow'

    def merge(self, savefile):
        files = os.path.join("E:\\dir1\\h3rc\\cpt_codes\\data\\", "*.csv")
        files = glob.glob(files)
        df = pd.concat(map(pd.read_csv, files), ignore_index = True)
        df = df.iloc[: , 1:]
        df = df.drop_duplicates()
        df.to_csv(savefile)

    # Function to select dates when a date range option exists
    def select_dates(self, start, end):
        date_from = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@id, "txtFrom")]')))
        date_from.clear()
        date_from.click()
        date_from.send_keys(start)
        date_to = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@id, "txtTo")]')))
        date_to.clear()
        date_to.click()
        date_to.send_keys(end)
        date_to.send_keys(Keys.ENTER)

    def set_date(self, date_option, date_from_val, date_to_val): 
        if date_option == 'Daily':
            self.select_dates(date_to_val, date_to_val)
        elif date_option == 'YTD':
            self.select_dates(date_from_val, date_to_val)
    
    # Splits a date range into processable day intervals to avoid downloads
    def date_range_gr30(self, startday, endday, day_intervals):
        start = datetime.strptime(startday,"%m-%d-%Y")
        end = datetime.strptime(endday,"%m-%d-%Y")
        diff = (end  - start)
        mod_diff = diff.days//day_intervals
    
        temp = []
        if diff.days > day_intervals:
            while mod_diff > 0:
                temp.append([start, start+timedelta(days=day_intervals)])
                start = (start+timedelta(days=day_intervals))
                mod_diff -=1
            temp.append([start, end])
        else:
            temp.append([start, end])

        res=[]
        for i in temp:
            res.append([j.strftime("%m-%d-%Y") for j in i])
        return res

    # Stages and runs a date range query and downloads the resulting data tables as temp csv's
    def stage_dr(self, date_from_val, date_to_val, day_intervals=28):
        split_range = self.date_range_gr30(date_from_val, date_to_val, day_intervals)
        cpt = CPTs_Report_Page(self.driver, self.wait)
        date_select = Select(self.wait.until(EC.element_to_be_clickable((By.ID, '_ctl0_ContentPlaceHolder1_ddltypes'))))
        date_select.select_by_value("R")

        for i,v in enumerate(split_range):
            self.set_date("YTD", v[0], v[1])
            # cpt.pull(savefile = f"E:\\dir1\\h3rc\\cpt_codes\\data\\{v[0]}_{v[1]}.csv")
            cpt.pull(savefile = f"E:\\dir1\\h3rc\\cpt_codes\\data\\temp{i}.csv")
    
    # Manual staging for situation when you want to use flask app
    def stage_dr_manual(self, savefile, date_from_val, date_to_val, day_intervals=28):
        split_range = self.date_range_gr30(date_from_val, date_to_val, day_intervals)
        cpt = CPTs_Report_Page(self.driver, self.wait)
        date_select = Select(self.wait.until(EC.element_to_be_clickable((By.ID, '_ctl0_ContentPlaceHolder1_ddltypes'))))
        date_select.select_by_value("R")

        for i,v in enumerate(split_range):
            self.set_date("YTD", v[0], v[1])
            # cpt.pull(savefile = f"E:\\dir1\\h3rc\\cpt_codes\\data\\{v[0]}_{v[1]}.csv")
            cpt.pull(savefile = f"{savefile}\\temp{i}.csv")
    
    def stage_month(self, month, year):
        sb = Select(self.wait.until(EC.element_to_be_clickable((By.ID, '_ctl0_ContentPlaceHolder1_ddltypes'))))
        sb.select_by_value("M")
        mo_select = Select(self.wait.until(EC.element_to_be_clickable((By.ID, '_ctl0_ContentPlaceHolder1_ddlmonth'))))
        mo_select.select_by_visible_text(str(month))
        yr_select = Select(self.wait.until(EC.element_to_be_clickable((By.ID, '_ctl0_ContentPlaceHolder1_ddlyear'))))
        yr_select.select_by_visible_text(str(year))
    
        run = self.driver.find_element(By.XPATH, '//*[@id="_ctl0_ContentPlaceHolder1_Runitnow"]')
        run.click()

        cpt = CPTs_Report_Page(self.driver, self.wait)
        cpt.pull(savefile = f"E:\\dir1\\h3rc\\cpt_codes\\data\\pull.csv")

    # Navigates to each patient chart in a list of patient charts then pulls the demogrpahic data from each patient chart
    def stage_demo(self, chart_ls):
        patient = Patient_Demo_Page(self.driver, self.wait)
        nav = Navigate(self.driver, self.wait)
        df = []
        for i in chart_ls:
            nav.open_patient_file(str(i))
            temp = patient.pull_patient_data()
            temp.update({"Chart #" : i})
            df.append(temp)
        pd.DataFrame(df).to_csv(f"E:\\dir1\\h3rc\\cpt_codes\\data\\pull{i}.csv")
            # cpt.pull(savefile = f"C:\\dir1\\cpt_codes\\data\\temp{i}.csv")