import pytest
import logging
from config.settings import settings

class TestPurchase:
    """Test cases for complete purchase flow"""
    
    @pytest.mark.smoke
    def test_complete_purchase_flow(self, login_page):
        """Test complete purchase flow"""
        # Login and add product
        products_page = login_page.login(
            settings.TEST_USERS["standard"]["username"],
            settings.TEST_USERS["standard"]["password"]
        )
        
        products_page.add_product_to_cart(0)
        cart_page = products_page.go_to_cart()
        
        # Start checkout
        checkout_page = cart_page.go_to_checkout()
        
        # Fill checkout information
        checkout_page.fill_checkout_info("John", "Doe", "12345")
        checkout_page.continue_to_overview()
        
        # Verify summary information
        summary = checkout_page.get_all_summary()
        assert summary['item_total'] > 0
        assert summary['tax'] > 0
        assert summary['total'] == summary['item_total'] + summary['tax']
        
        # Complete purchase
        checkout_page.finish_purchase()
        
        # Verify success
        assert checkout_page.is_order_complete()
        assert "THANK YOU FOR YOUR ORDER" in checkout_page.get_complete_message()
    
    def test_checkout_validation(self, login_page):
        """Test checkout form validation"""
        products_page = login_page.login(
            settings.TEST_USERS["standard"]["username"],
            settings.TEST_USERS["standard"]["password"]
        )
        
        products_page.add_product_to_cart(0)
        cart_page = products_page.go_to_cart()
        checkout_page = cart_page.go_to_checkout()
        
        # Try to continue without filling info
        checkout_page.continue_to_overview()
        
        # Verify error message
        error_message = checkout_page.get_error_message()
        assert error_message is not None
        assert "First Name" in error_message
    
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