from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from .base_page import BasePage
import logging

class ProductsPage(BasePage):
    # Locators
    TITLE = (By.CLASS_NAME, "title")
    PRODUCT_ITEM = (By.CLASS_NAME, "inventory_item")
    PRODUCT_NAME = (By.CLASS_NAME, "inventory_item_name")
    PRODUCT_DESC = (By.CLASS_NAME, "inventory_item_desc")
    PRODUCT_PRICE = (By.CLASS_NAME, "inventory_item_price")
    ADD_TO_CART_BUTTON = (By.CSS_SELECTOR, "button.btn_inventory")
    REMOVE_BUTTON = (By.CSS_SELECTOR, "button.btn_inventory.btn_secondary")
    CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
    CART_LINK = (By.CLASS_NAME, "shopping_cart_link")
    
    # Sorting
    SORT_DROPDOWN = (By.CLASS_NAME, "product_sort_container")
    
    # Menu
    MENU_BUTTON = (By.ID, "react-burger-menu-btn")
    LOGOUT_LINK = (By.ID, "logout_sidebar_link")
    ALL_ITEMS_LINK = (By.ID, "inventory_sidebar_link")
    
    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
        self.logger = logging.getLogger(__name__)
    
    def get_title(self):
        return self.get_text(self.TITLE)
    
    def get_products_count(self):
        products = self.driver.find_elements(*self.PRODUCT_ITEM)
        return len(products)
    
    def get_product_details(self, product_index=0):
        """Get details of specific product"""
        products = self.driver.find_elements(*self.PRODUCT_ITEM)
        
        if product_index >= len(products):
            raise IndexError(f"Product index {product_index} out of range")
        
        product = products[product_index]
        
        details = {
            'name': product.find_element(*self.PRODUCT_NAME).text,
            'description': product.find_element(*self.PRODUCT_DESC).text,
            'price': product.find_element(*self.PRODUCT_PRICE).text,
            'is_in_cart': self._is_add_to_cart_button(product)
        }
        
        return details
    
    def _is_add_to_cart_button(self, product_element):
        """Check if button is 'Add to cart' (not 'Remove')"""
        button = product_element.find_element(By.CSS_SELECTOR, "button")
        return "Add to cart" in button.text
    
    def add_product_to_cart(self, product_index=0):
        self.logger.info(f"Adding product #{product_index} to cart")
        products = self.driver.find_elements(*self.PRODUCT_ITEM)
        
        if product_index < len(products):
            product = products[product_index]
            button = product.find_element(By.CSS_SELECTOR, "button")
            
            if "Add to cart" in button.text:
                button.click()
                product_name = product.find_element(*self.PRODUCT_NAME).text
                self.logger.info(f"Added to cart: {product_name}")
                return True
        return False
    
    def add_product_by_name(self, product_name):
        """Add product to cart by its name"""
        products = self.driver.find_elements(*self.PRODUCT_ITEM)
        
        for product in products:
            name_element = product.find_element(*self.PRODUCT_NAME)
            if name_element.text == product_name:
                button = product.find_element(By.CSS_SELECTOR, "button")
                if "Add to cart" in button.text:
                    button.click()
                    self.logger.info(f"Added to cart: {product_name}")
                    return True
        return False
    
    def remove_product_from_cart(self, product_index=0):
        """Remove product from cart (from products page)"""
        products = self.driver.find_elements(*self.PRODUCT_ITEM)
        
        if product_index < len(products):
            product = products[product_index]
            button = product.find_element(By.CSS_SELECTOR, "button")
            
            if "Remove" in button.text:
                button.click()
                product_name = product.find_element(*self.PRODUCT_NAME).text
                self.logger.info(f"Removed from cart: {product_name}")
                return True
        return False
    
    def get_cart_count(self):
        try:
            return int(self.get_text(self.CART_BADGE))
        except:
            return 0
    
    def go_to_cart(self):
        self.click_element(self.CART_LINK)
        self.logger.info("Navigating to cart")
        
        from pages.cart_page import CartPage
        return CartPage(self.driver)
    
    def sort_products(self, sort_by="az"):
        """
        Sort products by option
        Options: "az" (A to Z), "za" (Z to A), 
                 "lohi" (low to high), "hilo" (high to low)
        """
        sort_options = {
            "az": "Name (A to Z)",
            "za": "Name (Z to A)",
            "lohi": "Price (low to high)",
            "hilo": "Price (high to low)"
        }
        
        if sort_by in sort_options:
            dropdown = Select(self.find_element(self.SORT_DROPDOWN))
            dropdown.select_by_visible_text(sort_options[sort_by])
            self.logger.info(f"Sorted products by: {sort_options[sort_by]}")
    
    def logout(self):
        """Logout from application"""
        self.click_element(self.MENU_BUTTON)
        # Wait for menu to appear
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        wait = WebDriverWait(self.driver, 5)
        wait.until(EC.element_to_be_clickable(self.LOGOUT_LINK))
        
        self.click_element(self.LOGOUT_LINK)
        self.logger.info("User logged out")
        
        from pages.login_page import LoginPage
        return LoginPage(self.driver)
    
    def get_all_products_details(self):
        """Get details of all products on page"""
        products_count = self.get_products_count()
        all_products = []
        
        for i in range(products_count):
            all_products.append(self.get_product_details(i))
        
        return all_products