import pytest
import logging

class TestLogin:
    @pytest.fixture
    def test_successful_login(self, login_page, test_data):
        """Test successful login with valid credentials"""
        products_page = login_page.login("standard_user", "secret_sauce")
        assert products_page.get_title() == "Products"
    
    @pytest.fixture
    def test_login_locked_user(self, login_page):
        """Test login attempt with locked out user"""
        login_page.login("locked_out_user", "secret_sauce")
        error_message = login_page.get_error_message()
        assert "Sorry, this user has been locked out" in error_message
    
    @pytest.fixture
    def test_login_invalid_credentials(self, login_page, test_data):
        """Test login with invalid credentials"""
        fake_user = test_data.generate_user()
        login_page.login(fake_user["username"], fake_user["password"])
        error_message = login_page.get_error_message()
        assert "Username and password do not match" in error_message