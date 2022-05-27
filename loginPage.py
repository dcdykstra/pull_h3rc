from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

class LoginPage():
    def __init__(self, driver, wait) -> None:   
        self.driver = driver
        self.wait = wait
        self.username_id = 'email'
        self.password_id = 'password'
        self.login_btn_id = "SigninBtn"
    
    def enter_username(self, username):
        self.driver.find_element(By.ID, self.username_id).clear()
        self.driver.find_element(By.ID, self.username_id).send_keys(username)
    
    def enter_password(self, password):
        self.driver.find_element(By.ID, self.password_id).clear()
        self.driver.find_element(By.ID, self.password_id).send_keys(password)

    def click_login(self):
        login = self.driver.find_element(By.ID, self.login_btn_id)
        login.click()
        
        try: 
            cont = self.wait.until(EC.element_to_be_clickable((By.ID, 'btnContinueLogin')))
            cont.click()
        except:
            print("No multiple logins - continue")