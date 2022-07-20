# eMed Web Scraper

### app.py
Flask app that creates a form to input values like login, password, report page, date range, and cpt codes

### run.py
Script to manually run code without having to use a Flask app

### loginPage.py
Used to log a user in

Functions include:

  + enter_username(username)
  + enter_password(password)
  + click_login(): Clicks the login button

### navigate.py
Used to navigate between report pages, patient demographic data, and iframes in eMed

### stage.py
Used to stage report pages and submit data requests. For example, it will run a report based on a date range and then save those reports to a certain save file.

### cpt_report.py
Used to scrape data from the eMed Report page "Services Reports -> CPTs Report"

Functions include:

  + make_soup(): Pulls the HTML data from the current webpage
  
  + enter_cpt_code(cpt_code): Used to enter a string of CPT codes into the proper text box. enter_cpt_code("12345", "54321")
  
  + pull(savefile): Pulls the data currently on the webpage and saves it to a location. pull("C:\\Code\\data")

### encounter_provider_report.py
Used to scrape data from the eMed Report page "Encounter Provider Reports -> Detailed Report"

Functions include:

  + make_soup(): Pulls the HTML data from the current webpage
  
  + deselect_ep(): Unchecks the Encounter Provider checkbox
  
  + select_ep(name): Selects a certain Provider by name
