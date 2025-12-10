import pytest
import logging
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.settings import settings

logger = logging.getLogger(__name__)

class TestPurchase:
    """Test cases for complete purchase flow"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup before each test"""
        # Принудительно устанавливаем chrome если обнаружен путь VS Code
        if hasattr(settings, 'BROWSER') and "/vscode/" in str(settings.BROWSER):
            settings.BROWSER = "chrome"
            logger.info(f"VS Code fix applied in test setup")

    @pytest.mark.smoke
    def test_complete_purchase_flow(self, login_page):
        """Test complete purchase flow"""
        logger.info(f"Starting purchase test with browser: {settings.BROWSER}")
        
        # Login and add product
        products_page = login_page.login("standard_user", "secret_sauce")
        
        products_page.add_product_to_cart(0)
        cart_page = products_page.go_to_cart()
        
        # Start checkout
        checkout_page = cart_page.go_to_checkout()
        
        # Fill checkout information
        checkout_page.fill_checkout_info("John", "Doe", "12345")
        checkout_page.continue_to_overview()
        
        # Verify summary information
        summary = checkout_page.get_all_summary()
        assert summary['item_total'] > 0, "Item total should be greater than 0"
        assert summary['tax'] > 0, "Tax should be greater than 0"
        assert summary['total'] == summary['item_total'] + summary['tax'], \
            f"Total {summary['total']} should equal item_total + tax"
        
        # Complete purchase
        checkout_page.finish_purchase()
        
        # Verify success
        assert checkout_page.is_order_complete(), "Order should be complete"
        complete_message = checkout_page.get_complete_message()
        assert "THANK YOU" in complete_message.upper(), \
            f"Complete message should contain 'THANK YOU', got: {complete_message}"
    
    def test_checkout_validation(self, login_page):
        """Test checkout form validation"""
        products_page = login_page.login("standard_user", "secret_sauce")
        
        products_page.add_product_to_cart(0)
        cart_page = products_page.go_to_cart()
        checkout_page = cart_page.go_to_checkout()
        
        # Try to continue without filling info
        checkout_page.continue_to_overview()
        
        # Verify error message
        error_message = checkout_page.get_error_message()
        assert error_message is not None, "Error message should be displayed"
        assert "First Name" in error_message or "required" in error_message, \
            f"Error message should mention required fields, got: {error_message}"
    
    def test_cancel_checkout(self, login_page):
        """Test canceling checkout"""
        products_page = login_page.login(
            settings.TEST_USERS["standard"]["username"],
            settings.TEST_USERS["standard"]["password"]
        )
        
        products_page.add_product_to_cart(0)
        cart_page = products_page.go_to_cart()
        checkout_page = cart_page.go_to_checkout()
        
        # Cancel checkout
        cart_page = checkout_page.cancel_checkout()
        
        # Verify we're back in cart
        assert not cart_page.is_empty()
    
    def test_back_home_after_purchase(self, login_page):
        """Test back home button after purchase"""
        products_page = login_page.login(
            settings.TEST_USERS["standard"]["username"],
            settings.TEST_USERS["standard"]["password"]
        )
        
        # Complete purchase
        products_page.add_product_to_cart(0)
        cart_page = products_page.go_to_cart()
        checkout_page = cart_page.go_to_checkout()
        checkout_page.fill_checkout_info("John", "Doe", "12345")
        checkout_page.continue_to_overview()
        checkout_page.finish_purchase()
        
        # Click back home
        products_page = checkout_page.back_to_home()
        
        # Verify we're on products page
        assert products_page.get_title() == "Products"