from models.store import StoreModel
from tests.unit.unit_base_test import UnitBasetest

class StoreTest(UnitBasetest):
    def test_create_store(self):
        store = StoreModel('storeName')

        self.assertEqual(store.name, 'storeName')

