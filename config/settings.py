"""
Configuration settings for the automation project.
All environment-specific settings are stored here.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file if exists
load_dotenv()

class Settings:
    """Main settings class for the automation framework"""
    
    # =========== APPLICATION SETTINGS ===========
    BASE_URL = os.getenv("BASE_URL", "https://www.saucedemo.com")
    TIMEOUT = int(os.getenv("TIMEOUT", "10"))
    
    # =========== BROWSER SETTINGS ===========
    BROWSER = os.getenv("BROWSER", "chrome").lower()
    HEADLESS = os.getenv("HEADLESS", "false").lower() == "true"
    WINDOW_SIZE = os.getenv("WINDOW_SIZE", "1920,1080")
    IMPLICIT_WAIT = int(os.getenv("IMPLICIT_WAIT", "10"))
    PAGE_LOAD_TIMEOUT = int(os.getenv("PAGE_LOAD_TIMEOUT", "30"))
    
    # Browser capabilities
    CHROME_OPTIONS = {
        "acceptInsecureCerts": True,
        "unhandledPromptBehavior": "accept",
        "args": [
            "--no-sandbox",
            "--disable-dev-shm-usage",
            "--disable-gpu",
            "--disable-extensions",
            "--disable-infobars",
            "--start-maximized"
        ]
    }
    
    FIREFOX_OPTIONS = {
        "acceptInsecureCerts": True,
        "unhandledPromptBehavior": "accept",
        "args": ["--width=1920", "--height=1080"]
    }
    
    # =========== TEST USERS ===========
    TEST_USERS = {
        "standard": {
            "username": os.getenv("STANDARD_USER", "standard_user"),
            "password": os.getenv("STANDARD_PASSWORD", "secret_sauce")
        },
        "locked": {
            "username": "locked_out_user",
            "password": "secret_sauce"
        },
        "problem": {
            "username": "problem_user",
            "password": "secret_sauce"
        },
        "performance": {
            "username": "performance_glitch_user",
            "password": "secret_sauce"
        }
    }
    
    # =========== SELENOID/SELENIUM GRID ===========
    USE_SELENOID = os.getenv("USE_SELENOID", "false").lower() == "true"
    SELENOID_HUB = os.getenv("SELENOID_HUB", "http://localhost:4444/wd/hub")
    SELENOID_CAPABILITIES = {
        "enableVNC": os.getenv("ENABLE_VNC", "true").lower() == "true",
        "enableVideo": os.getenv("ENABLE_VIDEO", "false").lower() == "true",
        "enableLog": os.getenv("ENABLE_LOG", "true").lower() == "true",
        "screenResolution": os.getenv("SCREEN_RESOLUTION", "1920x1080x24"),
        "timeZone": os.getenv("TIMEZONE", "Europe/Moscow")
    }
    
    # =========== DATABASE SETTINGS ===========
    # (For projects with DB verification)
    DB_ENABLED = os.getenv("DB_ENABLED", "false").lower() == "true"
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = int(os.getenv("DB_PORT", "5432"))
    DB_NAME = os.getenv("DB_NAME", "test_db")
    DB_USER = os.getenv("DB_USER", "postgres")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
    
    # =========== API SETTINGS ===========
    # (For API testing integration)
    API_BASE_URL = os.getenv("API_BASE_URL", "https://api.saucedemo.com")
    API_TIMEOUT = int(os.getenv("API_TIMEOUT", "10"))
    
    # =========== TEST DATA SETTINGS ===========
    DEFAULT_PRODUCT_COUNT = int(os.getenv("DEFAULT_PRODUCT_COUNT", "6"))
    TEST_DATA_SEED = os.getenv("TEST_DATA_SEED", "12345")
    
    # =========== PATHS AND DIRECTORIES ===========
    PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    LOGS_DIR = os.path.join(PROJECT_ROOT, "logs")
    REPORTS_DIR = os.path.join(PROJECT_ROOT, "reports")
    SCREENSHOTS_DIR = os.path.join(PROJECT_ROOT, "screenshots")
    DOWNLOADS_DIR = os.path.join(PROJECT_ROOT, "downloads")
    
    # =========== REPORTING SETTINGS ===========
    ALLURE_RESULTS = os.path.join(REPORTS_DIR, "allure-results")
    HTML_REPORT = os.path.join(REPORTS_DIR, "html", "report.html")
    ALLURE_HISTORY = os.path.join(REPORTS_DIR, "allure-history")
    
    GENERATE_ALLURE_REPORT = os.getenv("GENERATE_ALLURE", "true").lower() == "true"
    GENERATE_HTML_REPORT = os.getenv("GENERATE_HTML", "true").lower() == "true"
    SAVE_SCREENSHOTS = os.getenv("SAVE_SCREENSHOTS", "on_failure").lower()
    
    # =========== TEST EXECUTION SETTINGS ===========
    MAX_RETRIES = int(os.getenv("MAX_RETRIES", "2"))
    RETRY_DELAY = int(os.getenv("RETRY_DELAY", "2"))
    PARALLEL_WORKERS = int(os.getenv("PARALLEL_WORKERS", "1"))
    TEST_TIMEOUT = int(os.getenv("TEST_TIMEOUT", "300"))  # seconds
    
    # =========== ENVIRONMENT SPECIFIC ===========
    ENVIRONMENT = os.getenv("ENVIRONMENT", "development").lower()
    
    # Environment-specific overrides
    if ENVIRONMENT == "production":
        HEADLESS = True
        USE_SELENOID = True
        SAVE_SCREENSHOTS = "on_failure"
    elif ENVIRONMENT == "staging":
        HEADLESS = True
        SAVE_SCREENSHOTS = "on_failure"
    elif ENVIRONMENT == "development":
        HEADLESS = False
        SAVE_SCREENSHOTS = "always"
    
    # =========== VALIDATION ===========
    @classmethod
  
    def validate(cls):
        """Validate critical settings"""
        errors = []
        
        browser_str = str(cls.BROWSER).lower()
        if "/vscode/" in browser_str or "/helpers/browser" in browser_str:
           cls.BROWSER = "chrome"
           print(f"INFO: Browser normalized from '{browser_str}' to '{cls.BROWSER}' for CI environment")

        # Validate browser
        if cls.BROWSER not in ["chrome", "firefox", "edge"]:
            errors.append(f"Invalid browser: {cls.BROWSER}")
        
        # Validate environment
        if cls.ENVIRONMENT not in ["development", "staging", "production"]:
            errors.append(f"Invalid environment: {cls.ENVIRONMENT}")
        
        # Validate users
        if not cls.TEST_USERS["standard"]["username"]:
            errors.append("Standard user username is not set")
        
        if errors:
        # сообщение с подсчетом ошибок
          error_count = len(errors)
          formatted_errors = '\n  • '.join(errors)
          raise ValueError(
              f"Found {error_count} configuration error(s):\n  • {formatted_errors}"
              )

        return True
    
    @classmethod
    def get_browser_capabilities(cls):
        """Get browser capabilities based on settings"""
        capabilities = {}
        
        if cls.BROWSER == "chrome":
            capabilities.update(cls.CHROME_OPTIONS)
            if cls.HEADLESS:
                capabilities["args"].append("--headless=new")
        elif cls.BROWSER == "firefox":
            capabilities.update(cls.FIREFOX_OPTIONS)
            if cls.HEADLESS:
                capabilities["args"].append("--headless")
        
        if cls.USE_SELENOID:
            capabilities.update(cls.SELENOID_CAPABILITIES)
        
        return capabilities
    
    @classmethod
    def setup_directories(cls):
        """Create necessary directories"""
        directories = [
            cls.LOGS_DIR,
            cls.REPORTS_DIR,
            cls.SCREENSHOTS_DIR,
            cls.DOWNLOADS_DIR,
            cls.ALLURE_RESULTS,
            os.path.dirname(cls.HTML_REPORT)
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
        
        return True


# Create global settings instance
settings = Settings()

# Initialize directories
settings.setup_directories()

# Validate settings on import
settings.validate()