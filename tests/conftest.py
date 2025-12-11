# tests/conftest.py
import pytest
import time
import os
import stat
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import warnings

def get_chrome_driver_path():
    """Получить корректный путь к chromedriver с учетом новой структуры архива"""
    
    # Установка через WebDriverManager
    driver_path = ChromeDriverManager().install()
    
    # Путь к директории с драйвером
    driver_dir = os.path.dirname(driver_path)
    
    # Проверяем новую структуру (chromedriver внутри подпапки)
    possible_paths = [
        os.path.join(driver_dir, "chromedriver-linux64", "chromedriver"),
        os.path.join(driver_dir, "chromedriver"),
        driver_path
    ]
    
    # Ищем исполняемый файл
    for path in possible_paths:
        if os.path.exists(path):
            # Делаем файл исполняемым
            os.chmod(path, stat.S_IRWXU | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH)
            print(f"✓ Найден ChromeDriver: {path}")
            return path
    
    raise FileNotFoundError(f"ChromeDriver не найден. Проверенные пути: {possible_paths}")

@pytest.fixture(scope="function")
def driver():
    """Фикстура для создания драйвера и открытия saucedemo.com"""
    
    print("\n" + "="*60)
    print("ИНИЦИАЛИЗАЦИЯ ДРАЙВЕРА")
    print("="*60)
    
    # Получаем правильный путь к драйверу
    driver_path = get_chrome_driver_path()
    
    # Создаем сервис
    service = Service(driver_path)
    
    # Настройки Chrome для GitHub Codespaces
    options = Options()
    options.add_argument("--headless=new")  # Режим без графического интерфейса
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    
    # КРИТИЧЕСКИ ВАЖНЫЕ НАСТРОЙКИ ДЛЯ CODESPACES
    options.add_argument("--disable-software-rasterizer")
    options.add_argument("--no-zygote")
    options.add_argument("--single-process")
    options.add_argument("--disable-dev-shm-usage")
    
    # Отключаем блокировку headless-браузеров
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36")
    
    # Игнорируем SSL ошибки (на всякий случай)
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--ignore-ssl-errors")
    
    # Создаем драйвер
    print("Создаем драйвер Chrome...")
    driver = webdriver.Chrome(service=service, options=options)
    
    # КОНТРОЛЬНАЯ ТОЧКА: Устанавливаем таймаут загрузки страницы
    driver.set_page_load_timeout(30)
    driver.set_script_timeout(30)
    
    # ОТКРЫВАЕМ SAUCEDEMO.COM
    target_url = "https://www.saucedemo.com/"
    print(f"\nОткрываем: {target_url}")
    
    try:
        # 1. Пробуем стандартный GET
        driver.get(target_url)
        print(f"✓ Страница запрошена")
        
        # 2. Ждем загрузки
        time.sleep(3)  # Фиксированная задержка для стабильности
        
        # 3. Проверяем, что загрузилось
        print(f"✓ Текущий URL: {driver.current_url}")
        print(f"✓ Заголовок страницы: '{driver.title}'")
        
        # 4. Проверяем, что это действительно saucedemo.com
        if driver.current_url == "data:,":
            print("❌ КРИТИЧЕСКАЯ ОШИБКА: Загружена пустая страница data:,")
            print("   Пробуем альтернативный подход с явным ожиданием...")
            
            # Пробуем еще раз с другим подходом
            driver.execute_script("window.location.href = 'https://www.saucedemo.com/';")
            time.sleep(5)
            print(f"   Новый URL: {driver.current_url}")
        
        # 5. Делаем скриншот для диагностики
        screenshot_path = "/tmp/saucedemo_check.png"
        driver.save_screenshot(screenshot_path)
        print(f"✓ Скриншот сохранен: {screenshot_path}")
        
        # 6. Быстрая проверка элементов
        try:
            # Ищем любой контент на странице
            body = driver.find_element("tag name", "body")
            print(f"✓ Найдено тело страницы, текст: '{body.text[:100]}...'")
            
            # Считаем элементы
            all_elements = driver.find_elements("xpath", "//*")
            print(f"✓ Всего элементов на странице: {len(all_elements)}")
            
            inputs = driver.find_elements("tag name", "input")
            print(f"✓ Input элементов: {len(inputs)}")
            
            if len(inputs) > 0:
                for i, inp in enumerate(inputs[:3]):
                    print(f"  Input #{i+1}: id='{inp.get_attribute('id')}', "
                          f"type='{inp.get_attribute('type')}'")
            
        except Exception as e:
            print(f"⚠️  Не удалось найти элементы: {e}")
            
    except Exception as e:
        print(f"❌ ОШИБКА при загрузке страницы: {e}")
        
        # Пробуем загрузить простую страницу для проверки драйвера
        print("\nПробуем загрузить example.com для диагностики...")
        try:
            driver.get("http://example.com")
            time.sleep(2)
            print(f"✓ Example.com загружен: {driver.current_url}")
            print(f"✓ Заголовок: '{driver.title}'")
            
            if "saucedemo.com" not in driver.current_url:
                print("\n⚠️  ВНИМАНИЕ: Драйвер работает, но saucedemo.com недоступен.")
                print("   Возможные причины:")
                print("   1. Проблемы с сетью в Codespace")
                print("   2. Сайт временно недоступен")
                print("   3. Блокировка headless-браузеров")
                
                # Сохраняем HTML для анализа
                html_path = "/tmp/page_source.html"
                with open(html_path, "w", encoding="utf-8") as f:
                    f.write(driver.page_source[:2000])
                print(f"✓ HTML сохранен: {html_path}")
                
        except Exception as e2:
            print(f"❌ Даже example.com не загружается: {e2}")
            driver.quit()
            raise
    
    print("\n" + "="*60)
    yield driver
    
    print("\nЗакрываем драйвер...")
    driver.quit()
    print("="*60)

@pytest.fixture
def base_url():
    """Базовый URL приложения"""
    return "https://www.saucedemo.com/"

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
    """Фикстура LoginPage (для обратной совместимости)"""
    from pages.login_page import LoginPage
    return LoginPage(driver)