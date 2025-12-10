import pytest
from selenium.webdriver.common.by import By
from pages.login_page import LoginPage

class TestLogin:
    def test_successful_login(self, driver):
        """Тест успешного входа"""
        login_page = LoginPage(driver)
        login_page.login('standard_user', 'secret_sauce')
        
        # Проверяем, что мы на странице продуктов
        assert "inventory.html" in driver.current_url
        assert driver.find_element(By.CLASS_NAME, "inventory_list").is_displayed()
        
    def test_login_invalid_credentials(self, driver):
        """Тест входа с неверными данными"""
        login_page = LoginPage(driver)
        login_page.login('invalid_user', 'wrong_password')
        
        # Проверяем сообщение об ошибке
        error_message = login_page.get_error_message()
        assert "Username and password do not match" in error_message
        
    def test_login_locked_user(self, driver):
        """Тест входа заблокированным пользователем"""
        login_page = LoginPage(driver)
        login_page.login('locked_out_user', 'secret_sauce')
        
        # Проверяем сообщение об ошибке
        error_message = login_page.get_error_message()
        assert "Sorry, this user has been locked out" in error_message