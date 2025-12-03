import pytest
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from utils.logger import setup_logger
from utils.data_generator import TestDataGenerator

def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome", help="Browser to run tests: chrome or firefox")
    parser.addoption("--headless", action="store_true", help="Run in headless mode")

@pytest.fixture(scope="session")
def test_data():
    return TestDataGenerator()

@pytest.fixture
def driver(request):
    browser = request.config.getoption("--browser")
    headless = request.config.getoption("--headless")
    
    if browser == "chrome":
        options = Options()
        if headless:
            options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        driver = webdriver.Chrome(options=options)
    elif browser == "firefox":
        # аналогично для Firefox
        driver = webdriver.Firefox()
    else:
        raise ValueError(f"Unsupported browser: {browser}")
    
    driver.implicitly_wait(10)
    driver.maximize_window()
    
    yield driver
    
    driver.quit()

@pytest.fixture
def login_page(driver):
    from pages.login_page import LoginPage
    return LoginPage(driver).open()