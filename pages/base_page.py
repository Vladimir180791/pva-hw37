# pages/base_page.py
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time

class BasePage:
    """Базовый класс для всех Page Object."""
    def __init__(self, driver, timeout=20):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def wait_for_element_visible(self, locator, timeout=None):
        """Дождаться видимости элемента (ЗАМЕНИТЕ find_element на этот метод)."""
        wait = self.wait if timeout is None else WebDriverWait(self.driver, timeout)
        try:
            element = wait.until(EC.visibility_of_element_located(locator))
            print(f"Элемент видим: {locator}")
            return element
        except TimeoutException:
            print(f"Элемент не стал видимым: {locator}")
            raise

    def find_element(self, locator, timeout=None):
        """Найти один элемент с ожиданием."""
        wait = self.wait if timeout is None else WebDriverWait(self.driver, timeout)
        try:
            element = wait.until(EC.presence_of_element_located(locator))
            print(f"Элемент найден: {locator}")
            return element
        except TimeoutException:
            print(f"\n=== ДИАГНОСТИКА: не найден элемент {locator} ===")
            print(f"Текущий URL: {self.driver.current_url}")
            print(f"Заголовок страницы: {self.driver.title}")
            raise TimeoutException(f"Не удалось найти элемент с локатором {locator}")

    def find_elements(self, locator, timeout=None):
        """Найти несколько элементов с ожиданием."""
        wait = self.wait if timeout is None else WebDriverWait(self.driver, timeout)
        try:
            elements = wait.until(EC.presence_of_all_elements_located(locator))
            print(f"Найдено элементов {len(elements)}: {locator}")
            return elements
        except TimeoutException:
            return []

    def enter_text(self, locator, text):
        """Ввести текст в поле."""
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)
        print(f"Введен текст в {locator}")

    def click_element(self, locator):
        """Кликнуть по элементу."""
        element = self.find_element(locator)
        element.click()
        print(f"Кликнут элемент {locator}")

    def get_text(self, locator):
        """Получить текст элемента."""
        element = self.find_element(locator)
        return element.text

    def is_element_visible(self, locator, timeout=5):
        """Проверить, видим ли элемент."""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False

    def wait_for_page_load(self, timeout=10):
        """Дождаться загрузки страницы."""
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda d: d.execute_script('return document.readyState') == 'complete'
            )
            print("Страница загружена полностью")
            return True
        except TimeoutException:
            print("Страница не загрузилась полностью")
            return False