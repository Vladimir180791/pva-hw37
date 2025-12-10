import pytest
import logging
import sys
import os

# Добавляем путь к корневой папке проекта
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.settings import settings

logger = logging.getLogger(__name__)


class TestCart:
    """Test cases for shopping cart functionality"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup before each test"""
        # Принудительно устанавливаем chrome если обнаружен путь VS Code
        if hasattr(settings, 'BROWSER') and "/vscode/" in str(settings.BROWSER):
            settings.BROWSER = "chrome"
            logger.info(f"VS Code fix: Browser set to 'chrome'")

    @pytest.fixture
    def test_add_product_to_cart(self, login_page):
        """Test adding a product to cart"""
        # Login
        products_page = login_page.login(
            settings.TEST_USERS["standard"]["standard_user"],
            settings.TEST_USERS["standard"]["secret_sauce"]
        )
        
        logger.info(f"Testing with browser: {settings.BROWSER}")
        
        # Login
        products_page = login_page.login(username, password)
        
        # Add product to cart
        initial_count = products_page.get_cart_count()
        success = products_page.add_product_to_cart(0)
        
        assert success, "Failed to add product to cart"
        
        # Verify cart count increased
        new_count = products_page.get_cart_count()
        assert new_count == initial_count + 1, \
            f"Cart count should be {initial_count + 1}, but got {new_count}"
        
        # Go to cart and verify product is there
        cart_page = products_page.go_to_cart()
        assert not cart_page.is_empty(), "Cart should not be empty"
        assert cart_page.get_items_count() == 1, "Cart should have 1 item"

        # Add product to cart
        initial_count = products_page.get_cart_count()
        products_page.add_product_to_cart(0)
        
        # Verify cart count increased
        assert products_page.get_cart_count() == initial_count + 1
        
        # Go to cart and verify product is there
        cart_page = products_page.go_to_cart()
        assert not cart_page.is_empty()
        assert cart_page.get_items_count() == 1
        
        # Verify product details
        item_details = cart_page.get_item_details(0)
        assert item_details['name'] is not None
        assert item_details['price'] is not None
    
    @pytest.fixture
    def test_remove_product_from_cart(self, login_page):
        """Test removing product from cart"""
        products_page = login_page.login(
            settings.TEST_USERS["standard"]["standard_user"],
            settings.TEST_USERS["standard"]["secret_sauce"]
        )
        
        products_page = login_page.login(username, password)
        
        # Add two products
        products_page.add_product_to_cart(0)
        products_page.add_product_to_cart(1)
        
        cart_count = products_page.get_cart_count()
        assert cart_count == 2, f"Expected 2 items in cart, got {cart_count}"
        
        # Go to cart and remove one
        cart_page = products_page.go_to_cart()
        cart_page.remove_item(0)
        
        # Verify only one item remains
        remaining_items = cart_page.get_items_count()
        assert remaining_items == 1, f"Expected 1 item remaining, got {remaining_items}"
    
    @pytest.fixture
    def test_continue_shopping(self, login_page):
        """Test continue shopping button"""
        products_page = login_page.login(
            settings.TEST_USERS["standard"]["username"],
            settings.TEST_USERS["standard"]["password"]
        )
        
        # Add product and go to cart
        products_page.add_product_to_cart(0)
        cart_page = products_page.go_to_cart()
        
        # Continue shopping and verify we're back on products page
        products_page = cart_page.continue_shopping()
        assert products_page.get_title() == "Products"
    
    @pytest.fixture
    def test_empty_cart(self, login_page):
        """Test cart is empty initially"""
        products_page = login_page.login(
            settings.TEST_USERS["standard"]["username"],
            settings.TEST_USERS["standard"]["password"]
        )
        
        # Go to cart without adding items
        cart_page = products_page.go_to_cart()
        
        # Verify cart is empty
        assert cart_page.is_empty()
        assert cart_page.get_items_count() == 0
    
    @pytest.fixture
    def test_cart_total_calculation(self, login_page):
        """Test cart total price calculation"""
        products_page = login_page.login(
            settings.TEST_USERS["standard"]["username"],
            settings.TEST_USERS["standard"]["password"]
        )
        
        # Add two products
        products_page.add_product_to_cart(0)
        products_page.add_product_to_cart(1)
        
        # Get product prices
        product1 = products_page.get_product_details(0)
        product2 = products_page.get_product_details(1)
        
        # Calculate expected total
        price1 = float(product1['price'].replace('$', ''))
        price2 = float(product2['price'].replace('$', ''))
        expected_total = round(price1 + price2, 2)
        
        # Go to cart and verify total
        cart_page = products_page.go_to_cart()
        actual_total = cart_page.get_total_price()
        
        assert actual_total == expected_total