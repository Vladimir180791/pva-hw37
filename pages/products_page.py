from selenium.webdriver.common.by import By
from .base_page import BasePage

class ProductsPage(BasePage):
    # Locators
    TITLE = (By.CLASS_NAME, "title")
    PRODUCT_ITEM = (By.CLASS_NAME, "inventory_item")
    ADD_TO_CART_BUTTON = (By.CSS_SELECTOR, "button.btn_inventory")
    CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
    CART_LINK = (By.CLASS_NAME, "shopping_cart_link")
    
    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
    
    def get_title(self):
        return self.get_text(self.TITLE)
    
    def add_product_to_cart(self, product_index=0):
        self.logger.info(f"Adding product #{product_index} to cart")
        add_buttons = self.driver.find_elements(*self.ADD_TO_CART_BUTTON)
        add_buttons[product_index].click()
    
    def get_cart_count(self):
        try:
            return int(self.get_text(self.CART_BADGE))
        except:
            return 0
    
    def go_to_cart(self):
        self.click_element(self.CART_LINK)
        from pages.cart_page import CartPage
        return CartPage(self.driver)