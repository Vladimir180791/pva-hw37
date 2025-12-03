from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from .base_page import BasePage
import logging

class CartPage(BasePage):
    """Page Object for Shopping Cart page"""
    
    # Locators
    CART_ITEM = (By.CLASS_NAME, "cart_item")
    ITEM_NAME = (By.CLASS_NAME, "inventory_item_name")
    ITEM_DESC = (By.CLASS_NAME, "inventory_item_desc")
    ITEM_PRICE = (By.CLASS_NAME, "inventory_item_price")
    REMOVE_BUTTON = (By.CSS_SELECTOR, "button.cart_button")
    CONTINUE_SHOPPING_BTN = (By.ID, "continue-shopping")
    CHECKOUT_BUTTON = (By.ID, "checkout")
    QUANTITY_LABEL = (By.CLASS_NAME, "cart_quantity")
    
    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
        self.logger = logging.getLogger(__name__)
    
    def is_empty(self):
        """Check if cart is empty"""
        try:
            items = self.driver.find_elements(*self.CART_ITEM)
            return len(items) == 0
        except NoSuchElementException:
            return True
    
    def get_items_count(self):
        """Get number of items in cart"""
        try:
            items = self.driver.find_elements(*self.CART_ITEM)
            return len(items)
        except NoSuchElementException:
            return 0
    
    def get_item_details(self, item_index=0):
        """Get details of specific cart item"""
        items = self.driver.find_elements(*self.CART_ITEM)
        
        if item_index >= len(items):
            raise IndexError(f"Item index {item_index} out of range. Cart has {len(items)} items")
        
        item = items[item_index]
        
        details = {
            'name': item.find_element(*self.ITEM_NAME).text,
            'description': item.find_element(*self.ITEM_DESC).text,
            'price': item.find_element(*self.ITEM_PRICE).text,
            'quantity': item.find_element(*self.QUANTITY_LABEL).text
        }
        
        self.logger.info(f"Got item details: {details['name']} - {details['price']}")
        return details
    
    def get_all_items_details(self):
        """Get details of all items in cart"""
        items_count = self.get_items_count()
        all_items = []
        
        for i in range(items_count):
            all_items.append(self.get_item_details(i))
        
        return all_items
    
    def remove_item(self, item_index=0):
        """Remove item from cart"""
        items_before = self.get_items_count()
        
        items = self.driver.find_elements(*self.CART_ITEM)
        if item_index < len(items):
            remove_btn = items[item_index].find_element(*self.REMOVE_BUTTON)
            item_name = items[item_index].find_element(*self.ITEM_NAME).text
            remove_btn.click()
            self.logger.info(f"Removed item: {item_name}")
        
        # Wait for cart to update
        from time import sleep
        sleep(0.5)  # Можно заменить на явное ожидание
        
        items_after = self.get_items_count()
        return items_before - items_after == 1
    
    def remove_all_items(self):
        """Remove all items from cart"""
        items_count = self.get_items_count()
        
        for i in range(items_count):
            self.remove_item(0)  # Always remove first item as list changes
        
        return self.is_empty()
    
    def go_to_checkout(self):
        """Click checkout button and go to checkout page"""
        self.click_element(self.CHECKOUT_BUTTON)
        self.logger.info("Proceeding to checkout")
        
        from pages.checkout_page import CheckoutPage
        return CheckoutPage(self.driver)
    
    def continue_shopping(self):
        """Click continue shopping button"""
        self.click_element(self.CONTINUE_SHOPPING_BTN)
        self.logger.info("Continuing shopping")
        
        from pages.products_page import ProductsPage
        return ProductsPage(self.driver)
    
    def get_total_price(self):
        """Calculate total price of all items in cart"""
        items = self.get_all_items_details()
        total = 0.0
        
        for item in items:
            # Convert price string to float (remove $ sign)
            price_str = item['price'].replace('$', '').strip()
            total += float(price_str)
        
        return round(total, 2)
    
    def is_item_in_cart(self, item_name):
        """Check if specific item is in cart"""
        try:
            items = self.get_all_items_details()
            for item in items:
                if item['name'] == item_name:
                    return True
            return False
        except:
            return False