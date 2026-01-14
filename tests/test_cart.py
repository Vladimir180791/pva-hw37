import pytest
from selenium.webdriver.common.by import By
from pages.login_page import LoginPage
from pages.products_page import ProductsPage
from pages.cart_page import CartPage

class TestCart:
    @pytest.fixture(autouse=True)
    def setup(self, driver):
        self.driver = driver
        self.login_page = LoginPage(driver)
        self.products_page = ProductsPage(driver)
        self.cart_page = CartPage(driver)
        
        # Логин перед каждым тестом корзины
        self.login_page.login('standard_user', 'secret_sauce')
        
    def test_add_product_to_cart(self):
        """Тест добавления товара в корзину"""
        # Добавляем товар
        self.products_page.add_to_cart('Sauce Labs Backpack')
        
        # Переходим в корзину
        self.products_page.go_to_cart()
        
        # Проверяем, что товар в корзине
        cart_items = self.cart_page.get_cart_items()
        assert len(cart_items) == 1
        assert 'Sauce Labs Backpack' in cart_items[0]['name']
        
    def test_remove_product_from_cart(self):
        """Тест удаления товара из корзины"""
        # Добавляем товар
        self.products_page.add_to_cart('Sauce Labs Backpack')
        
        # Удаляем товар
        self.products_page.remove_from_cart('Sauce Labs Backpack')
        
        # Проверяем, что корзина пуста
        cart_badge = self.driver.find_elements(By.CLASS_NAME, "shopping_cart_badge")
        assert len(cart_badge) == 0  # Значок корзины не отображается
        
    def test_cart_total_calculation(self):
        """Тест расчета общей суммы в корзине"""
        # Добавляем несколько товаров
        self.products_page.add_to_cart('Sauce Labs Backpack')  # $29.99
        self.products_page.add_to_cart('Sauce Labs Bike Light')  # $9.99
        
        # Переходим в корзину
        self.products_page.go_to_cart()
        
        # Получаем общую сумму
        total = self.cart_page.get_total_amount()
        
        # Проверяем расчет (29.99 + 9.99 = 39.98)
        assert total == 39.98, f"Expected 39.98, got {total}"