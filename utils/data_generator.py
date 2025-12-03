from faker import Faker
import logging

class TestDataGenerator:
    def __init__(self):
        self.fake = Faker()
        self.logger = logging.getLogger(__name__)
    
    def generate_user(self):
        user = {
            "username": self.fake.user_name(),
            "password": self.fake.password(),
            "email": self.fake.email(),
            "first_name": self.fake.first_name(),
            "last_name": self.fake.last_name(),
            "zip_code": self.fake.zipcode(),
            "address": self.fake.address()
        }
        self.logger.info(f"Generated test user: {user['first_name']} {user['last_name']}")
        return user
    
    def generate_checkout_info(self):
        """Generate checkout information specifically for checkout tests"""
        return {
            "first_name": self.fake.first_name(),
            "last_name": self.fake.last_name(),
            "postal_code": self.fake.zipcode()
        }
    
    def generate_product_data(self):
        return {
            "name": self.fake.word().title(),
            "price": round(self.fake.random_number(digits=2) / 10, 2),
            "description": self.fake.sentence()
        }