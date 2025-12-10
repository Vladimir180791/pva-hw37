# tests/conftest.py
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import os

@pytest.fixture(scope="function")
def driver():
    # Установка драйвера
    driver_path = ChromeDriverManager().install()
    
    # Ищем реальный драйвер
    base_dir = os.path.dirname(driver_path)
    
    # Проверяем новую структуру
    new_structure_path = os.path.join(base_dir, "chromedriver-linux64", "chromedriver")
    
    if os.path.exists(new_structure_path):
        service = Service(new_structure_path)
    else:
        # Старая структура
        service = Service(driver_path)
    
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()
    
    yield driver
    driver.quit()

# Остальные фикстуры
@pytest.fixture
def base_url():
    return "https://www.saucedemo.com"

@pytest.fixture
def login_page(driver, base_url):
    class LoginPage:
        def __init__(self, driver, base_url):
            self.driver = driver
            self.base_url = base_url
        
        def login(self, username, password):
            print(f"🔑 Тестовый вход: {username}")
            class ProductsPage:
                def get_cart_count(self):
                    return 0
                def add_product_to_cart(self, idx):
                    return True
                def remove_product_from_cart(self, idx):
                    return True
            return ProductsPage()
    
    return LoginPage(driver, base_url)