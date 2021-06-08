import json

from models.item import ItemModel
from models.store import StoreModel
from tests.base_test import BaseTest


class StoreTest(BaseTest):

    # Man hittar "/store/test" i "App"
    # statuskod 201 = created success
    def test_create_store(self):
        with self.app() as client:
            with self.app_context():
                # Skapas store med namnet test?
                response = client.post('/store/test')

                # kontrollera att statuskoden från response är 201
                self.assertEqual(response.status_code, 201)

                # Kontrollera att det finns en store i databasen med namnet test
                self.assertIsNotNone(StoreModel.find_by_name('test'))

                # Kolla att datan från response är json med namn test och tom lista items?
                self.assertDictEqual({'name': 'test', 'items': []},
                                     json.loads(response.data))

    def test_create_duplicate_store(self):
        with self.app() as client:
            with self.app_context():
                client.post('/store/test')
                response = client.post('/store/test')

                # kontrollera att status_code blir 400 som angivet i resources/store (post)
                self.assertEqual(response.status_code, 400)

                # Kontrollera att felmeddelandet visas som anges i resources/store
                self.assertDictEqual({'message': "A store with name 'test' already exists."},
                                     json.loads(response.data))

    def test_delete_store(self):
        with self.app() as client:
            with self.app_context():
                # Lägger till store med namnet test
                StoreModel('test').save_to_db()

                # Kontrollerar att det finns en store med namnet test i databasen
                self.assertIsNotNone(StoreModel.find_by_name('test'))

                # Tar bort "test" store
                client.delete('/store/test')
                response = client.delete('/store/test')

                # Kollar så där inte finns något objekt med namn test i databasen
                self.assertIsNone(StoreModel.find_by_name('test'))
                self.assertDictEqual({'message': 'Store deleted'}, json.loads(response.data))

                # Kollar att respons-statuskod är 200 (HTTP kod för "OK")
                self.assertEqual(response.status_code, 200)

    def test_find_store(self):
        with self.app() as client:
            with self.app_context():
                # Se till att det först finns en Store tillagd att leta efter
                StoreModel('test').save_to_db()
                response = client.get('/store/test')

                # Kolla att statuskod är 200
                self.assertEqual(response.status_code, 200)

                # Kolla om där finns en store med det namnet
                self.assertIsNotNone(StoreModel.find_by_name('test'))

                # Se till att store returneras som json
                self.assertDictEqual({'name': 'test', 'items': []}, json.loads(response.data))

    def test_store_not_found(self):
        with self.app() as client:
            with self.app_context():
                # Getmetoden för att hämta store (som inte finns)
                response = client.get('/store/test')

                # Kontrollera att statuskod 404 visas ("Not found")
                self.assertEqual(response.status_code, 404)
                # Kontrollera att angett felmeddelande visas
                self.assertDictEqual(json.loads(response.data), {'message': 'Store not found'})

    def test_store_found_with_items(self):
        with self.app() as client:
            with self.app_context():
                # Lägg till Store och items till storen
                StoreModel('testStore').save_to_db()
                ItemModel('testItem1', 20, 1).save_to_db()

                response = client.get('/store/testStore')

                # Kolla att statuskod är 200
                self.assertEqual(response.status_code, 200)

                # Se till att store returneras som json
                self.assertDictEqual({'name': 'testStore', 'items': [{'name': 'testItem1', 'price': 20.0}]},
                                     json.loads(response.data))

    def test_store_list(self):
        with self.app() as client:
            with self.app_context():

                # Lägg till två stores i databasen
                StoreModel('test1').save_to_db()
                StoreModel('test2').save_to_db()

                response = client.get('/stores')

                self.assertDictEqual(json.loads(response.data),
                                     {'stores': [{'items': [], 'name': 'test1'}, {'items': [], 'name': 'test2'}]})

    def test_store_list_with_items(self):
        with self.app() as client:
            with self.app_context():

                # Lägg till två stores i databasen
                StoreModel('test1').save_to_db()
                StoreModel('test2').save_to_db()

                # Lägg till items
                ItemModel('testItem1', 20, 1).save_to_db()
                ItemModel('testItem2', 25, 2).save_to_db()

                response = client.get('/stores')

                self.assertDictEqual(json.loads(response.data),
                                     {'stores': [{'items': [{'name': 'testItem1', 'price': 20.0}], 'name': 'test1'},
                                                 {'items': [{'name': 'testItem2', 'price': 25.0}], 'name': 'test2'}]})
