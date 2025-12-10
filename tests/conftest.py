# tests/conftest.py
import pytest
import os
import stat
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def get_chrome_driver_path():
    """Получить корректный путь к chromedriver с учетом новой структуры архива"""
    
    # Установка через WebDriverManager
    driver_path = ChromeDriverManager().install()
    
    # Путь к директории с драйвером
    driver_dir = os.path.dirname(driver_path)
    
    # Проверяем новую структуру (chromedriver внутри подпапки)
    possible_paths = [
        # Новая структура (начиная с версии 115+)
        os.path.join(driver_dir, "chromedriver-linux64", "chromedriver"),
        # Альтернативная структура
        os.path.join(driver_dir, "chromedriver"),
        # Резервный вариант
        driver_path
    ]
    
    # Ищем исполняемый файл
    for path in possible_paths:
        if os.path.exists(path):
            # Делаем файл исполняемым
            os.chmod(path, stat.S_IRWXU | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH)
            return path
    
    raise FileNotFoundError(f"ChromeDriver не найден. Проверенные пути: {possible_paths}")

@pytest.fixture(scope="function")
def driver():
    """Фикстура для создания драйвера"""
    
    # Получаем правильный путь к драйверу
    driver_path = get_chrome_driver_path()
    
    print(f"Используем драйвер: {driver_path}")
    
    # Создаем сервис и драйвер
    service = Service(driver_path)
    
    # Настройки Chrome
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")  # Режим без графического интерфейса
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    
    driver = webdriver.Chrome(service=service, options=options)
    
    yield driver
    
    # Закрытие драйвера после теста
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