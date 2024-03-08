from fastapi.testclient import TestClient
from tests.working_test_case import TestCaseFastAPI
from main import app
from extensions import matchservice;


class TestEndpointBoard(TestCaseFastAPI):

    def setUp(self) -> None:
        matchservice.matches = []
        self.client = TestClient(app)

    def test_move(self):
        with self.client.websocket_connect('/ws') as websocket2:
            websocket2.send_json({'action': 'lobby_create', 'player_name': 'host', 'lobby_name': 'lobby'})
            websocket2.receive_json()

            with self.client.websocket_connect('/ws') as websocket:
                websocket.send_json({'action': 'lobby_join', 'player_name': 'player2', 'lobby_name': 'lobby'})
                websocket2.receive_json()
                websocket.receive_json()

                websocket.send_json({'action': 'lobby_start_match', 'player_name': 'host', 'lobby_name': 'lobby'})
                turn = websocket.receive_json()

                if turn['match']['turn'] == 'player2':
                    websocket2.send_json({'action': 'match_roll_dice', 'match_name': 'lobby'})
                    websocket2.send_json({'action': 'match_move', 'match_name': 'lobby', 'pos_x': 6, 'pos_y': 1})
                    websocket2.send_json({'action': 'match_end_turn', 'player_name': 'host', 'match_name': 'lobby'})
                    websocket2.receive_json()
                    websocket2.receive_json()
                    websocket2.receive_json()
                    websocket2.receive_json()

                websocket.send_json({'action': 'match_roll_dice', 'match_name': 'lobby'})
                websocket.receive_json()  # Dice

                websocket.send_json({'action': 'match_move', 'match_name': 'lobby', 'pos_x': 1, 'pos_y': 6})
                json = websocket.receive_json()

                self.assertEqual(json['square'], 'Regular')

    def test_move_through_trap(self):
        with self.client.websocket_connect('/ws') as websocket2:
            websocket2.send_json({'action': 'lobby_create', 'player_name': 'host', 'lobby_name': 'lobby2'})
            websocket2.receive_json()

            with self.client.websocket_connect('/ws') as websocket:
                websocket.send_json({'action': 'lobby_join', 'player_name': 'player2', 'lobby_name': 'lobby2'})
                websocket2.receive_json()
                websocket.receive_json()

                websocket.send_json({'action': 'lobby_start_match', 'player_name': 'host', 'lobby_name': 'lobby2'})
                turn = websocket.receive_json()

                if turn['match']['turn'] == 'player2':
                    websocket2.send_json({'action': 'match_roll_dice', 'match_name': 'lobby2'})
                    websocket2.send_json({'action': 'match_move', 'match_name': 'lobby2', 'pos_x': 6, 'pos_y': 1})
                    websocket2.send_json({'action': 'match_end_turn', 'player_name': 'host', 'match_name': 'lobby2'})
                    websocket2.receive_json()
                    websocket2.receive_json()
                    websocket2.receive_json()
                    websocket2.receive_json()
                    websocket.receive_json()
                    websocket.receive_json()
                    websocket.receive_json()

                websocket.send_json({'action': 'match_roll_dice', 'match_name': 'lobby2'})
                websocket.receive_json()

                matchservice.get_match_by_name('lobby2')._current_roll = 6

                websocket.send_json({'action': 'match_move', 'match_name': 'lobby2', 'pos_x': 4, 'pos_y': 6})
                websocket.send_json({'action': 'match_move', 'match_name': 'lobby2', 'pos_x': 15, 'pos_y': 6})
                websocket.receive_json()
                json = websocket.receive_json()
                self.assertEqual(json['square'], 'Spider')
