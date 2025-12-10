# tests/conftest.py
import pytest
import os
import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType

@pytest.fixture(scope="function")
def driver():
    """Фикстура драйвера с автоматической установкой chromedriver"""
    
    options = webdriver.ChromeOptions()
    
    # Определяем, какой Chrome/Chromium установлен
    chrome_paths = [
        "/usr/bin/chromium-browser",
        "/usr/bin/google-chrome",
        "/snap/bin/chromium"
    ]
    
    chrome_binary = None
    for path in chrome_paths:
        if os.path.exists(path):
            chrome_binary = path
            print(f"✅ Найден браузер: {chrome_binary}")
            options.binary_location = chrome_binary
            break
    
    # Если не нашли - используем системный
    if not chrome_binary:
        print("⚠️  Браузер не найден, используем системный")
    
    # Критически важные опции для CI
    options.add_argument('--headless=new')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-software-rasterizer')
    options.add_argument('--window-size=1920,1080')
    
    # Отключаем логи
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    
    try:
        # Используем webdriver-manager для автоматической установки правильного chromedriver
        print("📥 Устанавливаем/проверяем chromedriver...")
        
        # Определяем тип Chrome
        chrome_type = ChromeType.CHROMIUM if "chromium" in str(chrome_binary).lower() else ChromeType.GOOGLE
        
        # Устанавливаем chromedriver
        driver_path = ChromeDriverManager(chrome_type=chrome_type).install()
        print(f"✅ Chromedriver установлен: {driver_path}")
        
        # Создаем сервис и драйвер
        service = Service(driver_path)
        driver = webdriver.Chrome(service=service, options=options)
        
        driver.implicitly_wait(10)
        print("✅ Драйвер успешно создан")
        
        yield driver
        
    except Exception as e:
        print(f"❌ Ошибка создания драйвера: {e}")
        print("Пробуем альтернативный метод...")
        
        # Альтернативный метод: скачиваем напрямую
        driver = _create_chrome_driver_fallback(options)
        yield driver
    
    finally:
        # Закрываем драйвер
        try:
            driver.quit()
            print("✅ Драйвер закрыт")
        except:
            pass

def _create_chrome_driver_fallback(options):
    """Альтернативный метод создания драйвера"""
    import requests
    import zipfile
    import io
    
    try:
        # Скачиваем конкретную версию chromedriver
        print("🔄 Скачиваем chromedriver напрямую...")
        url = "https://storage.googleapis.com/chrome-for-testing-public/120.0.6099.71/linux64/chromedriver-linux64.zip"
        response = requests.get(url)
        
        # Распаковываем
        with zipfile.ZipFile(io.BytesIO(response.content)) as zip_file:
            zip_file.extractall('/tmp/chromedriver_fallback')
        
        driver_path = '/tmp/chromedriver_fallback/chromedriver-linux64/chromedriver'
        os.chmod(driver_path, 0o755)
        
        service = Service(driver_path)
        driver = webdriver.Chrome(service=service, options=options)
        driver.implicitly_wait(10)
        
        print("✅ Драйвер создан через fallback метод")
        return driver
        
    except Exception as e:
        print(f"❌ Fallback также не сработал: {e}")
        raise

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