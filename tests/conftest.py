# Добавить новую фикстуру для корзины
@pytest.fixture
def cart_with_item(login_page):
    """Fixture that returns cart page with one item"""
    from config.settings import settings
    
    products_page = login_page.login(
        settings.TEST_USERS["standard"]["username"],
        settings.TEST_USERS["standard"]["password"]
    )
    
    products_page.add_product_to_cart(0)
    cart_page = products_page.go_to_cart()
    return cart_page

@pytest.fixture
def checkout_page_with_item(cart_with_item):
    """Fixture that returns checkout page with item in cart"""
    checkout_page = cart_with_item.go_to_checkout()
    return checkout_page