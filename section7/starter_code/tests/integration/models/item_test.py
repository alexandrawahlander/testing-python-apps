from models.item import ItemModel
from models.store import StoreModel
from tests.base_test import BaseTest


class ItemTest(BaseTest):

    def test_crud(self):
        with self.app_context():
            StoreModel('test').save_to_db()
            item = ItemModel('test', 19.99, 1)

            #Testa att objekt inte finns i databas ännu
            self.assertIsNone(ItemModel.find_by_name('test'),
                              "Found an item with name {}, but expected not to.".format(item.name))

            item.save_to_db()

            #Testa att objektet nu finns i databasen
            self.assertIsNotNone(ItemModel.find_by_name('test'))

            item.delete_from_db()

            #Testa att det fungerade att radera från databasen
            self.assertIsNone(ItemModel.find_by_name('test'))

    def test_crud_alex(self):
        with self.app_context():
            store = StoreModel('test')
            item = ItemModel('test', 19.99, 1)

            store.save_to_db()

            self.assertIsNone(ItemModel.find_by_name('test'),
                              "Found an item with name {}, but expected not to.".format(item.name))

            item.save_to_db()

            self.assertIsNotNone(ItemModel.find_by_name('test'))

            item.delete_from_db()
            store.delete_from_db()

            self.assertIsNone(ItemModel.find_by_name('test'))

    def test_store_relationship(self):
        with self.app_context():
            store = StoreModel('test_store')
            item = ItemModel('test', 19.99, 1)

            store.save_to_db()
            item.save_to_db()

            self.assertEqual(item.store.name, 'test_store')