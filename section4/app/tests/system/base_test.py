from unittest import TestCase
from app import app

class BaseTest(TestCase):
    def setUp(self):
        app.testing = True #Talar om för Flask att vi testar
        self.app = app.test_client
