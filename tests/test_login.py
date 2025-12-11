# tests/test_login.py
import pytest
from selenium.webdriver.common.by import By
from pages.login_page import LoginPage

class TestLogin:

    def test_successful_login(self, driver):
        """Тест успешного входа."""
        login_page = LoginPage(driver)
        
        print("\n" + "="*50)
        print("ТЕСТ: УСПЕШНЫЙ ВХОД")
        print("="*50)
        
        login_page.login("standard_user", "secret_sauce")
        
        # Проверяем, что мы перешли на страницу продуктов
        print(f"После логина URL: {driver.current_url}")
        assert "inventory" in driver.current_url, \
            f"Ожидался переход на inventory, но URL: {driver.current_url}"
        
        # Проверяем наличие элемента, характерного для страницы продуктов
        inventory_items = driver.find_elements(By.CLASS_NAME, "inventory_item")
        assert len(inventory_items) > 0, "Товары не найдены на странице продуктов"
        
        print(f"✓ Найдено товаров: {len(inventory_items)}")
        print("✅ Тест успешного входа пройден!")
        print("="*50)
    
    def test_login_invalid_credentials(self, driver):
        """Тест входа с неверными данными."""
        login_page = LoginPage(driver)
        
        print("\n" + "="*50)
        print("ТЕСТ: НЕВЕРНЫЕ УЧЕТНЫЕ ДАННЫЕ")
        print("="*50)
        
        login_page.login("invalid_user", "wrong_password")
        
        error_text = login_page.get_error_message()
        print(f"Текст ошибки: '{error_text}'")
        
        # Проверяем, что появилось сообщение об ошибке
        assert error_text != "", "Ожидалось сообщение об ошибке"
        assert "Username and password do not match" in error_text
        
        print("✅ Тест неверных учетных данных пройден!")
        print("="*50)
    
    def test_login_locked_user(self, driver):
        """Тест входа заблокированным пользователем."""
        login_page = LoginPage(driver)
        
        print("\n" + "="*50)
        print("ТЕСТ: ЗАБЛОКИРОВАННЫЙ ПОЛЬЗОВАТЕЛЬ")
        print("="*50)
        
        login_page.login("locked_out_user", "secret_sauce")
        
        error_text = login_page.get_error_message()
        print(f"Текст ошибки: '{error_text}'")
        
        assert "Sorry, this user has been locked out" in error_text
        
        print("✅ Тест заблокированного пользователя пройден!")
        print("="*50)