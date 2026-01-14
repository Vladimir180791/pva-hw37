import pytest
from pages.login_page import LoginPage
from pages.products_page import ProductsPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage

class TestPurchase:
    @pytest.fixture(autouse=True)
    def setup(self, driver):
        self.driver = driver
        self.login_page = LoginPage(driver)
        self.products_page = ProductsPage(driver)
        self.cart_page = CartPage(driver)
        self.checkout_page = CheckoutPage(driver)
        
        # Логин
        self.login_page.login('standard_user', 'secret_sauce')
        
    def test_complete_purchase_flow(self):
        """Тест полного процесса покупки"""
        # 1. Добавляем товар в корзину
        self.products_page.add_to_cart('Sauce Labs Backpack')
        
        # 2. Переходим в корзину
        self.products_page.go_to_cart()
        
        # 3. Проверяем товар в корзине
        cart_items = self.cart_page.get_cart_items()
        assert len(cart_items) == 1
        
        # 4. Начинаем оформление заказа
        self.cart_page.checkout()
        
        # 5. Заполняем информацию
        self.checkout_page.fill_checkout_info('John', 'Doe', '12345')
        
        # 6. Завершаем покупку
        self.checkout_page.finish_checkout()
        
        # 7. Проверяем подтверждение
        confirmation = self.checkout_page.get_confirmation_message()
        assert "Thank you for your order" in confirmation
        
        # 8. Проверяем, что корзина пуста (количество товаров = 0)
        cart_badge = self.driver.find_elements(By.CLASS_NAME, "shopping_cart_badge")
        if cart_badge:
            cart_count = int(cart_badge[0].text)
            assert cart_count == 0
        else:
            # Значок корзины не отображается, значит корзина пуста
            pass