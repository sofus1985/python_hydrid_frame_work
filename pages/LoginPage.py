from selenium.webdriver.common.by import By
from base.Base import Base

class LoginPage(Base):
    USERNAME_INPUT = (By.XPATH,"//input[@id='input-email']")
    PASSWORD_INPUT = (By.XPATH,"//input[@id='input-password']")
    LOGIN_BUTTON = (By.XPATH, "//input[@value='Login']")

    def enter_username(self, username):
        self.send_keys(self.USERNAME_INPUT, username)

    def enter_password(self, password):
        self.send_keys(self.PASSWORD_INPUT, password)

    def click_login(self):
        self.safe_click(self.LOGIN_BUTTON)

