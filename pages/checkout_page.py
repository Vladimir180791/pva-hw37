from selenium.webdriver.common.by import By
from .base_page import BasePage
import logging

class CheckoutPage(BasePage):
    """Page Object for Checkout pages (Step One, Step Two, Complete)"""
    
    # Step One: Your Information
    FIRST_NAME_INPUT = (By.ID, "first-name")
    LAST_NAME_INPUT = (By.ID, "last-name")
    POSTAL_CODE_INPUT = (By.ID, "postal-code")
    CONTINUE_BUTTON = (By.ID, "continue")
    CANCEL_BUTTON = (By.ID, "cancel")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")
    
    # Step Two: Overview
    PAYMENT_INFO = (By.CLASS_NAME, "summary_value_label")  # First element
    SHIPPING_INFO = (By.CLASS_NAME, "summary_value_label")  # Second element
    ITEM_TOTAL = (By.CLASS_NAME, "summary_subtotal_label")
    TAX = (By.CLASS_NAME, "summary_tax_label")
    TOTAL = (By.CLASS_NAME, "summary_total_label")
    FINISH_BUTTON = (By.ID, "finish")
    
    # Step Three: Complete
    COMPLETE_HEADER = (By.CLASS_NAME, "complete-header")
    COMPLETE_TEXT = (By.CLASS_NAME, "complete-text")
    BACK_HOME_BUTTON = (By.ID, "back-to-products")
    
    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
        self.logger = logging.getLogger(__name__)
    
    # --- Step One Methods ---
    def fill_checkout_info(self, first_name, last_name, postal_code):
        """Fill checkout information form"""
        self.logger.info(f"Filling checkout info: {first_name} {last_name}, {postal_code}")
        
        self.enter_text(self.FIRST_NAME_INPUT, first_name)
        self.enter_text(self.LAST_NAME_INPUT, last_name)
        self.enter_text(self.POSTAL_CODE_INPUT, postal_code)
        
        return self
    
    def fill_checkout_info_from_dict(self, user_info):
        """Fill checkout information from dictionary"""
        return self.fill_checkout_info(
            user_info.get('first_name', ''),
            user_info.get('last_name', ''),
            user_info.get('postal_code', '')
        )
    
    def continue_to_overview(self):
        """Click continue to go to overview page"""
        self.click_element(self.CONTINUE_BUTTON)
        self.logger.info("Continuing to checkout overview")
        
        # Return self since we're still on CheckoutPage, just different step
        return self
    
    def cancel_checkout(self):
        """Cancel checkout and return to cart"""
        self.click_element(self.CANCEL_BUTTON)
        self.logger.info("Checkout cancelled")
        
        from pages.cart_page import CartPage
        return CartPage(self.driver)
    
    def get_error_message(self):
        """Get error message if validation fails"""
        try:
            return self.get_text(self.ERROR_MESSAGE)
        except:
            return None
    
    # --- Step Two Methods ---
    def get_payment_info(self):
        """Get payment information from overview"""
        elements = self.driver.find_elements(*self.PAYMENT_INFO)
        return elements[0].text if len(elements) > 0 else ""
    
    def get_shipping_info(self):
        """Get shipping information from overview"""
        elements = self.driver.find_elements(*self.SHIPPING_INFO)
        return elements[1].text if len(elements) > 1 else ""
    
    def get_item_total(self):
        """Get item total price"""
        total_text = self.get_text(self.ITEM_TOTAL)
        # Extract number from string like "Item total: $29.99"
        return self._extract_price(total_text)
    
    def get_tax(self):
        """Get tax amount"""
        tax_text = self.get_text(self.TAX)
        return self._extract_price(tax_text)
    
    def get_total(self):
        """Get total price with tax"""
        total_text = self.get_text(self.TOTAL)
        return self._extract_price(total_text)
    
    def _extract_price(self, text):
        """Helper method to extract price from text"""
        import re
        match = re.search(r'\$(\d+\.\d+)', text)
        return float(match.group(1)) if match else 0.0
    
    def get_all_summary(self):
        """Get all summary information as dictionary"""
        return {
            'payment_info': self.get_payment_info(),
            'shipping_info': self.get_shipping_info(),
            'item_total': self.get_item_total(),
            'tax': self.get_tax(),
            'total': self.get_total()
        }
    
    def finish_purchase(self):
        """Click finish button to complete purchase"""
        self.click_element(self.FINISH_BUTTON)
        self.logger.info("Finishing purchase")
        return self  # Now on complete page
    
    # --- Step Three Methods ---
    def get_complete_message(self):
        """Get completion message"""
        return self.get_text(self.COMPLETE_HEADER)
    
    def get_complete_text(self):
        """Get completion description text"""
        return self.get_text(self.COMPLETE_TEXT)
    
    def is_order_complete(self):
        """Check if order was completed successfully"""
        try:
            message = self.get_complete_message()
            return "THANK YOU FOR YOUR ORDER" in message.upper()
        except:
            return False
    
    def back_to_home(self):
        """Click back home button"""
        self.click_element(self.BACK_HOME_BUTTON)
        self.logger.info("Returning to home/products page")
        
        from pages.products_page import ProductsPage
        return ProductsPage(self.driver)
    
    # --- Combined flow methods ---
    def complete_purchase(self, first_name, last_name, postal_code):
        """Complete entire purchase flow"""
        self.fill_checkout_info(first_name, last_name, postal_code)
        self.continue_to_overview()
        self.finish_purchase()
        
        return self.is_order_complete()