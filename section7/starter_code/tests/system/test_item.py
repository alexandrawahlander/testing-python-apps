from models.store import StoreModel
from models.user import UserModel
from models.item import ItemModel
from tests.base_test import BaseTest
import json


class ItemTest(BaseTest):
    def setUp(self):
        super(ItemTest, self).setUp()
        with self.app() as client:
            with self.app_context():

                # Skapa en användare så att det går att logga in sen
                UserModel('test', '1234').save_to_db()
                auth_request = client.post('/auth',
                                           data=json.dumps({'username': 'test', 'password': '1234'}),
                                           headers={'Content-Type': 'application/json'})
                #auth_token = json.loads(auth_request.data)['access_token']

                #self.access_token = f'JWT {auth_token}'
                self.access_token = "JWT {}".format(json.loads(auth_request.data)['access_token'])

    def test_get_item_no_auth(self):
        with self.app() as client:
            #with self.app_context():
                response = client.get('/item/test')

                # status code 401 = Unauthorized
                self.assertEqual(response.status_code, 401)

    def test_get_item_not_found(self):
        with self.app() as client:
            with self.app_context():

                response = client.get('/item/test', headers={'Authorization': self.access_token})

                self.assertEqual(response.status_code, 404)

    def test_get_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 19.99, 1).save_to_db()
                response = client.get('/item/test', headers={'Authorization': self.access_token})

                self.assertEqual(response.status_code, 200)
                self.assertDictEqual(json.loads(response.data), {'name': 'test', 'price': 19.99})

    def test_delete_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 19.99, 1).save_to_db()

                response = client.delete('/item/test')
                self.assertEqual(response.status_code, 200)
                self.assertIsNone(ItemModel.find_by_name('test'))
                self.assertDictEqual(json.loads(response.data), {'message': 'Item deleted'})

    def test_create_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()

                response = client.post('/item/test', data={'price': 17.99, 'store_id': 1})

                self.assertEqual(response.status_code, 201)
                self.assertDictEqual({'name': 'test', 'price': 17.99},
                                     json.loads(response.data))

    def test_create_duplicate_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 17.99, 1).save_to_db()

                response = client.post('/item/test', data={'price': 17.99, 'store_id': 1})

                self.assertEqual(response.status_code, 400)
                self.assertDictEqual({'message': "An item with name 'test' already exists."},
                                     json.loads(response.data))

    # "Put" kan både lägga till item eller uppdatera ett item med ny data om det redan existerar
    def test_put_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()

                response = client.put('/item/test', data={'price': 17.99, 'store_id': 1})

                self.assertEqual(response.status_code, 200)
                self.assertEqual(ItemModel.find_by_name('test').price, 17.99)
                self.assertDictEqual({'name': 'test', 'price': 17.99},
                                     json.loads(response.data))

    def test_put_item_update(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 17.99, 1).save_to_db()

                self.assertEqual(ItemModel.find_by_name('test').price, 17.99)

                response = client.put('/item/test', data={'price': 16.99, 'store_id': 1})

                self.assertEqual(response.status_code, 200)
                self.assertEqual(ItemModel.find_by_name('test').price, 16.99)
                self.assertDictEqual({'name': 'test', 'price': 16.99},
                                     json.loads(response.data))

    def test_item_list(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                StoreModel('test2').save_to_db()
                ItemModel('test', 17.99, 1).save_to_db()
                ItemModel('test2', 18.99, 1).save_to_db()
                ItemModel('test3', 19.99, 2).save_to_db()

                response = client.get('/items')

                self.assertEqual(response.status_code, 200)
                self.assertDictEqual({'items': [{'name': 'test', 'price': 17.99},
                                                {'name': 'test2', 'price': 18.99},
                                                {'name': 'test3', 'price': 19.99}]},
                                     json.loads(response.data))
