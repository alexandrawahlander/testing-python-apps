from tests.system.base_test import BaseTest
import json

class TestHome(BaseTest):
    def test_home(self):
         with self.app() as c: #self.app är samma som app.test_client
            response = c.get('/')

            self.assertEqual(response.status_code, 200) #200 är standardstatus när allt är OK

            self.assertEqual(
                json.loads(response.get_data()), #Jämför denna raden
                {'message': 'Hello, world!'} #Med denna
            )
    #loads = load string
