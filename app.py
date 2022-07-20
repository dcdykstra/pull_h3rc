from flask import Flask, render_template, request
import pandas as pd
import json

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains 
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

import time
import pandas as pd

from loginPage import LoginPage
from navigate import Navigate
from cpt_report import CPTs_Report_Page
from stage import Stage
from encounter_provider_report import EP_DetReport_Page
from patient_report import Patient_Demo_Page
from niu import NIU
from xlsx_writer import XLSX

app = Flask(__name__)

@app.route('/')
def my_form():
    return render_template('myform.html')

@app.route('/', methods=['POST'])
def my_form_post():
    # reports_dict = pd.read_csv("report_pages.csv", index_col=0, squeeze=True).to_dict()

    username = request.form['username']
    pwd = request.form['pwd']
    report = request.form['report']
    code = request.form['code']
    datef = request.form['datef']
    dateto = request.form['dateto']
    savefile = request.form['savefile']


    prefs = {'profile.default_content_setting_values.automatic_downloads': 1}
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_experimental_option('prefs', prefs)
    driver = webdriver.Chrome(service = Service(ChromeDriverManager().install()), options=options)
    actions = ActionChains(driver)
    wait = WebDriverWait(driver, 20)

    driver.get("https://service.emedpractice.com/index.aspx")
    login = LoginPage(driver, wait)
    login.enter_username(str(username))
    login.enter_password(str(pwd)) 
    login.click_login()

    nav = Navigate(driver, wait)
    nav.nav_reports()
    nav.load_report(str(report))

    cpt = CPTs_Report_Page(driver, wait)
    cpt.enter_cpt_code(str(code))
        
    stage = Stage(driver, wait)
    stage.stage_dr_manual(savefile = savefile, date_from_val = str(datef), date_to_val = str(dateto), day_intervals = 28)
    time.sleep(5)

    element_text = driver.page_source
    driver.quit()
    return element_text

if __name__ == '__main__':
  app.run(debug=True)