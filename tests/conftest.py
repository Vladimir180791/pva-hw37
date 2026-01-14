# tests/conftest.py
import pytest
import time
import os
import sys
import stat
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import warnings

def get_chrome_driver_path():
    """Получить корректный путь к chromedriver с учетом платформы"""
    
    print("Получаем путь к ChromeDriver...")
    
    # Для Windows используем force_install=True и явно указываем версию
    try:
        # Используем фиксированную версию для стабильности
        driver_path = ChromeDriverManager(driver_version="114.0.5735.90").install()
    except Exception as e:
        print(f"Ошибка при установке ChromeDriver: {e}")
        # Пробуем без указания версии
        driver_path = ChromeDriverManager().install()
    
    print(f"WebDriverManager вернул путь: {driver_path}")
    
    # Проверяем, существует ли файл
    if os.path.exists(driver_path):
        print(f"✓ ChromeDriver найден по пути: {driver_path}")
        return driver_path
    
    # Если путь не существует, ищем драйвер в различных местах
    driver_dir = os.path.dirname(driver_path)
    
    # Возможные пути (в зависимости от платформы)
    possible_paths = []
    
    if sys.platform == "win32":  # Windows
        possible_paths = [
            os.path.join(driver_dir, "chromedriver.exe"),
            os.path.join(driver_dir, "chromedriver-win64", "chromedriver.exe"),
            os.path.join(driver_dir, "chromedriver-win32", "chromedriver.exe"),
            driver_path,
            r"C:\Windows\system32\config\systemprofile\.wdm\drivers\chromedriver\win64\latest\chromedriver.exe",
            r"C:\Users\jenkins\.wdm\drivers\chromedriver\win64\latest\chromedriver.exe"
        ]
    else:  # Linux/Mac
        possible_paths = [
            os.path.join(driver_dir, "chromedriver"),
            os.path.join(driver_dir, "chromedriver-linux64", "chromedriver"),
            os.path.join(driver_dir, "chromedriver-mac-arm64", "chromedriver"),
            driver_path
        ]
    
    print(f"Проверяем возможные пути: {possible_paths}")
    
    for path in possible_paths:
        if os.path.exists(path):
            # Для Unix-систем делаем файл исполняемым
            if sys.platform != "win32":
                try:
                    os.chmod(path, stat.S_IRWXU | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH)
                except Exception as e:
                    print(f"Не удалось изменить права файла: {e}")
            
            print(f"✓ ChromeDriver найден по альтернативному пути: {path}")
            return path
    
    # Если ничего не нашли, пробуем использовать webdriver-manager напрямую
    print("⚠️ ChromeDriver не найден в файловой системе. Пробуем альтернативный подход...")
    
    # Создаем временный драйвер для диагностики
    try:
        from webdriver_manager.core.os_manager import ChromeType
        
        driver_path = ChromeDriverManager(chrome_type=ChromeType.GOOGLE).install()
        print(f"✓ ChromeDriver получен через альтернативный метод: {driver_path}")
        return driver_path
    except Exception as e:
        print(f"❌ Все методы поиска ChromeDriver провалились: {e}")
        raise FileNotFoundError(f"ChromeDriver не найден. Проверенные пути: {possible_paths}")

@pytest.fixture(scope="function")
def driver():
    """Фикстура для создания драйвера и открытия saucedemo.com"""
    
    print("\n" + "="*60)
    print("ИНИЦИАЛИЗАЦИЯ ДРАЙВЕРА")
    print("="*60)
    
    # Получаем настройки из переменных окружения
    headless_mode = os.getenv("HEADLESS", "true").lower() == "true"
    browser = os.getenv("BROWSER", "chrome")
    
    print(f"Браузер: {browser}")
    print(f"Режим headless: {headless_mode}")
    
    if browser.lower() == "chrome":
        # Получаем правильный путь к драйверу
        driver_path = get_chrome_driver_path()
        
        # Создаем сервис
        service = Service(driver_path)
        
        # Настройки Chrome
        options = Options()
        
        if headless_mode:
            options.add_argument("--headless=new")
        
        # Общие настройки для стабильности
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        
        # Для Windows добавляем специфичные настройки
        if sys.platform == "win32":
            options.add_argument("--disable-software-rasterizer")
            options.add_argument("--disable-extensions")
            options.add_argument("--disable-logging")
            options.add_argument("--log-level=3")
        else:
            # Для Linux (Codespaces)
            options.add_argument("--no-zygote")
            options.add_argument("--single-process")
        
        # Отключаем блокировку автоматизации
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        # Игнорируем SSL ошибки
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--ignore-ssl-errors")
        
        # Создаем драйвер с обработкой ошибок
        print("Создаем драйвер Chrome...")
        try:
            driver = webdriver.Chrome(service=service, options=options)
            print("✓ Драйвер успешно создан")
        except Exception as e:
            print(f"❌ Ошибка при создании драйвера: {e}")
            print("Пробуем создать драйвер без сервиса...")
            try:
                driver = webdriver.Chrome(options=options)
                print("✓ Драйвер создан без сервиса")
            except Exception as e2:
                print(f"❌ Критическая ошибка: {e2}")
                print("Пробуем использовать Firefox как запасной вариант...")
                from selenium.webdriver.firefox.options import Options as FirefoxOptions
                from selenium.webdriver.firefox.service import Service as FirefoxService
                from webdriver_manager.firefox import GeckoDriverManager
                
                # Настраиваем Firefox
                firefox_options = FirefoxOptions()
                if headless_mode:
                    firefox_options.add_argument("--headless")
                
                firefox_service = FirefoxService(GeckoDriverManager().install())
                driver = webdriver.Firefox(service=firefox_service, options=firefox_options)
                print("✓ Драйвер Firefox создан")
    
    else:
        # Для Firefox
        from selenium.webdriver.firefox.options import Options as FirefoxOptions
        from selenium.webdriver.firefox.service import Service as FirefoxService
        from webdriver_manager.firefox import GeckoDriverManager
        
        firefox_options = FirefoxOptions()
        if headless_mode:
            firefox_options.add_argument("--headless")
        
        firefox_service = FirefoxService(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=firefox_service, options=firefox_options)
    
    # КОНТРОЛЬНАЯ ТОЧКА: Устанавливаем таймауты
    timeout = int(os.getenv("TIMEOUT", "30"))
    driver.set_page_load_timeout(timeout)
    driver.set_script_timeout(timeout)
    driver.implicitly_wait(10)
    
    # ОТКРЫВАЕМ SAUCEDEMO.COM
    base_url = os.getenv("BASE_URL", "https://www.saucedemo.com/")
    print(f"\nОткрываем: {base_url}")
    
    try:
        driver.get(base_url)
        print(f"✓ Страница запрошена")
        
        # Ждем загрузки
        time.sleep(2)
        
        print(f"✓ Текущий URL: {driver.current_url}")
        print(f"✓ Заголовок страницы: '{driver.title}'")
        
        # Делаем скриншот для диагностики
        try:
            screenshot_dir = os.path.join(os.getcwd(), "screenshots")
            os.makedirs(screenshot_dir, exist_ok=True)
            screenshot_path = os.path.join(screenshot_dir, "initial_page.png")
            driver.save_screenshot(screenshot_path)
            print(f"✓ Скриншот сохранен: {screenshot_path}")
        except Exception as e:
            print(f"⚠️ Не удалось сделать скриншот: {e}")
        
    except Exception as e:
        print(f"❌ ОШИБКА при загрузке страницы: {e}")
        
        # Пробуем загрузить тестовую страницу
        print("\nПробуем загрузить example.com для диагностики...")
        try:
            driver.get("http://example.com")
            time.sleep(2)
            print(f"✓ Example.com загружен: {driver.current_url}")
            print(f"✓ Заголовок: '{driver.title}'")
        except Exception as e2:
            print(f"❌ Критическая ошибка: {e2}")
            driver.quit()
            raise
    
    print("\n" + "="*60)
    yield driver
    
    print("\nЗакрываем драйвер...")
    try:
        driver.quit()
        print("✓ Драйвер закрыт")
    except Exception as e:
        print(f"⚠️ Ошибка при закрытии драйвера: {e}")
    
    print("="*60)

@pytest.fixture
def base_url():
    """Базовый URL приложения"""
    return os.getenv("BASE_URL", "https://www.saucedemo.com/")

@pytest.fixture
def user_credentials():
    """Тестовые учетные данные"""
    return {
        'standard_user': {'username': 'standard_user', 'password': 'secret_sauce'},
        'locked_user': {'username': 'locked_out_user', 'password': 'secret_sauce'},
        'problem_user': {'username': 'problem_user', 'password': 'secret_sauce'},
        'performance_user': {'username': 'performance_glitch_user', 'password': 'secret_sauce'}
    }

@pytest.fixture
def login_page(driver, base_url):
    """Фикстура LoginPage"""
    from pages.login_page import LoginPage
    return LoginPage(driver)