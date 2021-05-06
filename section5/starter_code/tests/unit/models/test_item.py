from unittest import TestCase
from models.item import ItemModel
from tests.base_test import baseTestItem

testItem = ItemModel('ItemName', 19.99)

class ItemTest(TestCase):

    def test_create_item(self):
        item = ItemModel('ItemName', 'ItemPrice')

        self.assertEqual('ItemName', item.name, "Namnet stämmer inte!")
        self.assertEqual('ItemPrice', item.price, "Priset överensstämmer inte!")

    def test_create_item2(self): #använder ett item skapat högst upp istället.

        self.assertEqual('ItemName', testItem.name)
        self.assertEqual(19.99, testItem.price)


    def test_item_json(self):
        item = ItemModel('ItemName', 25)
        expected = {'name': 'ItemName', 'price': 25}

        self.assertDictEqual(expected, item.json(), "The JSON export of the item is incorrect. Received {}, expected {}".format(item.json(), expected))


