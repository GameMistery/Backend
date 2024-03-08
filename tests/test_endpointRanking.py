from fastapi.testclient import TestClient
from main import app
from tests.working_test_case import TestCaseFastAPI
from ranking.ranking_db import * 

class TestRankingEndpoints(TestCaseFastAPI):

    def setUp(self) -> None:
        self.client = TestClient(app)

    def test_get_top_ten(self):
        with self.client.websocket_connect('/ws') as websocket:
            websocket.send_json({'action': 'ranking_get_top_ten'})
            data = websocket.receive_json()
            self.assertEqual(data['action'],'top-ten')