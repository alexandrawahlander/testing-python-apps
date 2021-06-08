from models.user import UserModel
from tests.base_test import BaseTest

class UserTest(BaseTest):
    def test_crud(self):
        with self.app_context():
            user = UserModel('unameTest', 'psw123')

        #Testa att man inte kan hitta användaren ännu, eftersom den inte sparats än
            self.assertIsNone(UserModel.find_by_username('unameTest'))
            self.assertIsNone(UserModel.find_by_id(1))

            user.save_to_db()

            self.assertIsNotNone(UserModel.find_by_username('unameTest'))
            self.assertIsNotNone(UserModel.find_by_id(1))



