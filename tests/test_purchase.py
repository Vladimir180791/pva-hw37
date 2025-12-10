import pytest
import logging

class TestPurchase:
    @pytest.fixture
    def test_complete_purchase_flow(self, login_page):
        """Test complete purchase flow from login to checkout"""
        # Login
        products_page = login_page.login("standard_user", "secret_sauce")
        
        # Add product to cart
        products_page.add_product_to_cart(0)
        assert products_page.get_cart_count() == 1
        
        # Go to cart and checkout
        cart_page = products_page.go_to_cart()
        checkout_page = cart_page.go_to_checkout()
        
        # Fill checkout information
        checkout_page.fill_checkout_info("John", "Doe", "12345")
        overview_page = checkout_page.continue_to_overview()
        
        # Complete purchase
        complete_page = overview_page.finish_purchase()
        
        # Verify success
        assert "Thank you for your order" in complete_page.get_success_message()