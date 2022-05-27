from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys

from cpt_report import CPTs_Report_Page
from datetime import datetime
from datetime import timedelta

class Stage():
    def __init__(self, driver, wait) -> None:
        self.driver = driver
        self.wait = wait
        self.run_btn_id = '_ctl0_ContentPlaceHolder1_btnRunItNow'

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
    
    # def stage_vr(self, date_option, date_from_val, date_to_val):
    #     self.set_date(date_option, date_from_val, date_to_val)

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

    def stage_dr(self, date_option, search_by, date_from_val, date_to_val, day_intervals=28):
        split_range = self.date_range_gr30(date_from_val, date_to_val, day_intervals)
        cpt = CPTs_Report_Page(self.driver, self.wait)
        date_select = Select(self.wait.until(EC.element_to_be_clickable((By.ID, '_ctl0_ContentPlaceHolder1_ddltypes'))))
        date_select.select_by_value(search_by)

        for i,v in enumerate(split_range):
            self.set_date(date_option, v[0], v[1])
            cpt.pull(savefile = f"E:\\dir1\\h3rc\\cpt_codes\\temp{i}.csv")
            # cpt.pull(savefile = f"C:\\dir1\\cpt_codes\\temp{i}.csv")