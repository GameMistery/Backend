from fastapi.testclient import TestClient
from tests.working_test_case import TestCaseFastAPI
from extensions import lobbyservice
from main import app


class TestEndpointChat(TestCaseFastAPI):

    def setUp(self):
        self.client = TestClient(app)

    def test_send_msg_lobby(self):
        with self.client.websocket_connect('/ws') as websocket:
            websocket.send_json({'action': 'lobby_create', 'player_name': 'host', 'lobby_name': 'send-msg-lobby'})
            websocket.receive_json()

            websocket.send_json({'action': 'chat_lobby_send', 'player_name': 'host',
                                 'chat_name': 'send-msg-lobby', 'message': "Test message"})
            data = websocket.receive_json()

            websocket.send_json({'action': 'lobby_leave', 'player_name': 'host', 'lobby_name': 'send-msg-lobby'})
            self.assertEqual(data['action'], 'new_message')

    def test_send_101_messages(self):
        with self.client.websocket_connect('/ws') as websocket:
            websocket.send_json({'action': 'lobby_create', 'player_name': 'host', 'lobby_name': 'send-101-msgs'})
            websocket.receive_json()

            lobby = lobbyservice.get_lobby_by_name('send-101-msgs')

            for i in range(0, 101):
                websocket.send_json({'action': 'chat_lobby_send', 'player_name': 'host',
                                     'chat_name': 'send-101-msgs', 'message': f"msg-{i}"})
                websocket.receive_json()
            
            last_msg = lobby.chat[0]
            websocket.send_json({'action': 'lobby_leave', 'player_name': 'host', 'lobby_name': 'send-101-msgs'})

            self.assertEqual(last_msg[-7:], "msg-100")

    def test_send_msg_msg(self):
        with self.client.websocket_connect('/ws') as websocket0:
            websocket0.send_json({'action': 'lobby_create', 'player_name': 'host', 'lobby_name': 'send-msg-match'})
            websocket0.receive_json()
            websocket0.send_json({'action': 'chat_lobby_send', 'player_name': 'host',
                                  'chat_name': 'send-msg-match', 'message': "Test message"})
            websocket0.receive_json()

            with self.client.websocket_connect('/ws') as websocket1:
                websocket1.send_json({'action': 'lobby_join', 'player_name':
                    'test-player', 'lobby_name': 'send-msg-match'})
                websocket0.receive_json()
                data = websocket1.receive_json()
                
                self.assertEqual(len(data['chat']), 1)

                websocket0.send_json({'action': 'lobby_start_match', 'player_name':
                    'host', 'lobby_name': 'send-msg-match'})
                websocket0.receive_json()
                data = websocket1.receive_json()

                self.assertEqual(len(data['chat']), 1)

                websocket0.send_json({'action': 'chat_match_send', 'player_name': 'host',
                                      'chat_name': 'send-msg-match', 'message': "match msg"})
                websocket0.receive_json()
                data = websocket1.receive_json()

                self.assertEqual(data['action'], 'new_message')