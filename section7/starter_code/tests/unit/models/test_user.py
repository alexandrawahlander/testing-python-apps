from models.user import UserModel
from tests.unit.unit_base_test import UnitBasetest

class UserTest(UnitBasetest):
    def test_create_user(self):
        user = UserModel('testUserName', 'psw123')

        self.assertEqual(user.username, 'testUserName')
        self.assertEqual(user.password, 'psw123')