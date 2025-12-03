import pytest
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.remote_connection import RemoteConnection

from config.settings import settings
from utils.logger import setup_logger

def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default=settings.BROWSER, 
                    help=f"Browser to run tests: {settings.BROWSER}")
    parser.addoption("--headless", action="store_true", default=settings.HEADLESS,
                    help="Run in headless mode")
    parser.addoption("--env", action="store", default=settings.ENVIRONMENT,
                    help=f"Environment: {settings.ENVIRONMENT}")

@pytest.fixture(scope="session")
def env_config(request):
    """Get environment configuration"""
    env = request.config.getoption("--env")
    # Можно добавить логику для загрузки разных конфигов по окружению
    return settings

@pytest.fixture
def driver(request, env_config):
    """WebDriver fixture with centralized configuration"""
    browser = request.config.getoption("--browser")
    headless = request.config.getoption("--headless")
    
    driver_instance = None
    
    try:
        if env_config.USE_SELENOID:
            driver_instance = _create_remote_driver(browser, env_config)
        else:
            driver_instance = _create_local_driver(browser, headless, env_config)
        
        # Set timeouts
        driver_instance.implicitly_wait(env_config.IMPLICIT_WAIT)
        driver_instance.set_page_load_timeout(env_config.PAGE_LOAD_TIMEOUT)
        
        # Set window size
        if not headless and not env_config.USE_SELENOID:
            width, height = map(int, env_config.WINDOW_SIZE.split(','))
            driver_instance.set_window_size(width, height)
        
        yield driver_instance
        
    finally:
        if driver_instance:
            driver_instance.quit()

def _create_local_driver(browser, headless, config):
    """Create local WebDriver instance"""
    if browser == "chrome":
        options = ChromeOptions()
        for arg in config.CHROME_OPTIONS.get("args", []):
            options.add_argument(arg)
        
        if headless:
            options.add_argument("--headless=new")
        
        return webdriver.Chrome(options=options)
    
    elif browser == "firefox":
        options = FirefoxOptions()
        for arg in config.FIREFOX_OPTIONS.get("args", []):
            options.add_argument(arg)
        
        if headless:
            options.add_argument("--headless")
        
        return webdriver.Firefox(options=options)
    
    else:
        raise ValueError(f"Unsupported browser: {browser}")

def _create_remote_driver(browser, config):
    """Create remote WebDriver for Selenoid/Grid"""
    from selenium.webdriver import Remote
    
    capabilities = {
        "browserName": browser,
        "version": "latest",
        "platform": "LINUX",
    }
    
    # Add browser-specific capabilities
    if browser == "chrome":
        capabilities.update(config.CHROME_OPTIONS)
    elif browser == "firefox":
        capabilities.update(config.FIREFOX_OPTIONS)
    
    # Add Selenoid capabilities
    capabilities.update(config.SELENOID_CAPABILITIES)
    
    # Clean capabilities for remote connection
    if "args" in capabilities:
        capabilities.pop("args")
    
    executor = RemoteConnection(config.SELENOID_HUB, resolve_ip=False)
    return Remote(
        command_executor=executor,
        desired_capabilities=capabilities
    )

@pytest.fixture
def base_url(env_config):
    """Base URL fixture"""
    return env_config.BASE_URL

@pytest.fixture
def test_user(env_config):
    """Get standard test user"""
    return env_config.TEST_USERS["standard"]

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook to take screenshot on test failure"""
    outcome = yield
    report = outcome.get_result()
    
    if report.when == "call" and report.failed:
        if "driver" in item.fixturenames:
            driver = item.funcargs["driver"]
            try:
                screenshot_dir = settings.SCREENSHOTS_DIR
                import os
                os.makedirs(screenshot_dir, exist_ok=True)
                
                test_name = item.name.replace("[", "_").replace("]", "_")
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                screenshot_path = os.path.join(
                    screenshot_dir, 
                    f"{test_name}_{timestamp}.png"
                )
                driver.save_screenshot(screenshot_path)
                logging.info(f"Screenshot saved: {screenshot_path}")
            except Exception as e:
                logging.error(f"Failed to take screenshot: {e}")