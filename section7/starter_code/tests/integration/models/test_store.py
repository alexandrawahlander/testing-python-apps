from models.item import ItemModel
from models.store import StoreModel

from tests.base_test import BaseTest


class StoreTest(BaseTest):
    def test_create_store_items_empty(self):
        with self.app_context():
            store = StoreModel('test')
            store.save_to_db()

            self.assertListEqual(store.items.all(), [], "Fel")

    def test_crud(self):  # Test create, read, update, delete
        with self.app_context():
            store = StoreModel('testName')

            self.assertIsNone(StoreModel.find_by_name('testName'))

            store.save_to_db()

            self.assertIsNotNone(StoreModel.find_by_name('testName'))

            store.delete_from_db()

            self.assertIsNone(StoreModel.find_by_name('testName'))

    def test_store_relationship(self):
        with self.app_context():
            store = StoreModel('test')
            item = ItemModel('test_item', 19.99, 1)

            store.save_to_db()
            item.save_to_db()

            self.assertEqual(store.items.count(), 1)
            self.assertEqual(store.items.first().name, 'test_item')

    def test_store_json(self):
        with self.app_context():
            store = StoreModel('test')
            store.save_to_db()
            expected = {
                'name': 'test',
                'items': []
            }

            self.assertEqual(store.json(), expected)

    def test_store_json_with_item(self):
        with self.app_context():
            store = StoreModel('test')
            item = ItemModel('test_item', 19.99, 1)

            store.save_to_db()
            item.save_to_db()

            expected = {
                'name': 'test',
                'items': [{'name': 'test_item', 'price': 19.99}]
            }

            self.assertDictEqual(store.json(), expected)
