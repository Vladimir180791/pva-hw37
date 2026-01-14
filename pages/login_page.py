# pages/login_page.py
from selenium.webdriver.common.by import By
from .base_page import BasePage
import time  # Убедитесь, что этот импорт есть!

class LoginPage(BasePage):
    """Page Object для страницы логина."""

    # ЛОКАТОРЫ для сайта https://www.saucedemo.com/
    USERNAME_INPUT = (By.ID, "user-name")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error'], .error-message, .error")

    def __init__(self, driver):
        super().__init__(driver)

    def login(self, username, password):
        """Выполнить вход."""
        # Ждем загрузки страницы
        self.wait_for_page_load()
        
        print(f"Ищу поле username с локатором: {self.USERNAME_INPUT}")
        
        # Ждем видимости полей
        self.wait_for_element_visible(self.USERNAME_INPUT, timeout=15)
        print("✓ Поле username найдено и видимо")
        
        # ИСПРАВЛЕНО: используем ПАРАМЕТРЫ метода, а не переменные!
        print(f"Ввожу username: '{username}'")
        self.enter_text(self.USERNAME_INPUT, username)  # Было: standard_user
        
        print(f"Ввожу password: '{password}'")
        self.enter_text(self.PASSWORD_INPUT, password)  # Было: secret_sauce
        
        print("Кликаю по кнопке логина")
        self.click_element(self.LOGIN_BUTTON)
        
        # Небольшая пауза после клика
        time.sleep(1)
        print("Логин выполнен, жду 1 секунду")

    def get_error_message(self):
        """Получить текст сообщения об ошибке."""
        if self.is_element_visible(self.ERROR_MESSAGE, timeout=5):
            return self.get_text(self.ERROR_MESSAGE)
        return ""