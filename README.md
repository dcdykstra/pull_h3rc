# eMed Web Scraper

### cpt_report.py
Used to scrape data from the eMed Report page "CPTs Report"
Functions include:

  make_soup(): Pulls the HTML data from the current webpage
  
  enter_cpt_code(cpt_code): Used to enter a string of CPT codes into the proper text box. enter_cpt_code("12345", "54321")
  
  pull(savefile): Pulls the data currently on the webpage and saves it to a location. pull("C:\\Code\\data")

### encounter_provider_report.py
