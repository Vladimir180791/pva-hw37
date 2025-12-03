import logging
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.logger = logging.getLogger(__name__)
        self.wait = WebDriverWait(driver, 10)
    
    def find_element(self, locator):
        self.logger.info(f"Finding element: {locator}")
        return self.wait.until(EC.presence_of_element_located(locator))
    
    def click_element(self, locator):
        self.logger.info(f"Clicking element: {locator}")
        element = self.find_element(locator)
        element.click()
    
    def enter_text(self, locator, text):
        self.logger.info(f"Entering text '{text}' into {locator}")
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)
    
    def get_text(self, locator):
        element = self.find_element(locator)
        text = element.text
        self.logger.info(f"Got text: '{text}' from {locator}")
        return text