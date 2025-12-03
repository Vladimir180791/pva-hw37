from selenium.webdriver.common.by import By
from .base_page import BasePage

class LoginPage(BasePage):
    # Locators
    USERNAME_INPUT = (By.ID, "user-name")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")
    
    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
    
    def open(self):
        self.driver.get("https://www.saucedemo.com/")
        return self
    
    def login(self, username, password):
        self.logger.info(f"Logging in with username: {username}")
        self.enter_text(self.USERNAME_INPUT, username)
        self.enter_text(self.PASSWORD_INPUT, password)
        self.click_element(self.LOGIN_BUTTON)
        from pages.products_page import ProductsPage
        return ProductsPage(self.driver)
    
    def get_error_message(self):
        return self.get_text(self.ERROR_MESSAGE)