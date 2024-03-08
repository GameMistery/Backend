from fastapi.testclient import TestClient
from main import app
from extensions import matchservice
from tests.working_test_case import TestCaseFastAPI
from util.vector import Vector2d


class TestMatchEndpoints(TestCaseFastAPI):

    def setUp(self) -> None:
        self.client = TestClient(app)

    def test_end_turn(self):
        with self.client.websocket_connect('/ws') as websocket:
            websocket.send_json({'action': 'lobby_create', 'player_name': 'host', 'lobby_name': 'test-end-turn'})
            websocket.receive_json()

            websocket.send_json({'action': 'lobby_join', 'player_name': 'test-player', 'lobby_name': 'test-end-turn'})
            #There are 2 receive per accion because there is one messege per player
            websocket.receive_json()
            websocket.receive_json()
            
            websocket.send_json({'action': 'lobby_start_match', 'player_name': 'host', 'lobby_name': 'test-end-turn'})
            websocket.receive_json()
            websocket.receive_json()

            for i in range(5):
                match = matchservice.get_match_by_name('test-end-turn')
                if(match.current_turn().nickname == 'host'):
                    websocket.send_json({'action': 'match_roll_dice', 'match_name': 'test-end-turn'})
                    websocket.send_json({'action': 'match_move', 'match_name': 'test-end-turn', 'pos_x': 1, 'pos_y': 6})
                    websocket.send_json({'action': 'match_end_turn', 'match_name': 'test-end-turn'})
                    websocket.receive_json()
                    websocket.receive_json()
                    websocket.receive_json()
                    websocket.receive_json()
                    websocket.receive_json()

                    data = websocket.receive_json()
                    self.assertEqual(data, {'action': 'turn_passed', 'current_turn': 'test-player'})
                else:
                    websocket.send_json({'action': 'match_roll_dice', 'match_name': 'test-end-turn'})
                    websocket.send_json({'action': 'match_move', 'match_name': 'test-end-turn', 'pos_x': 6, 'pos_y': 1})
                    websocket.send_json({'action': 'match_end_turn', 'match_name': 'test-end-turn'})

                    websocket.receive_json()
                    websocket.receive_json()
                    websocket.receive_json()
                    websocket.receive_json()
                    websocket.receive_json()
                    data = websocket.receive_json()
                    self.assertEqual(data, {'action': 'turn_passed', 'current_turn': 'host'})

    def test_get_hand(self):
        with self.client.websocket_connect('/ws') as websocket:
            websocket.send_json({'action': 'lobby_create', 'player_name': 'host', 'lobby_name': 'test-get-hand'})
            websocket.receive_json()

            websocket.send_json({'action': 'lobby_join', 'player_name': 'test-player', 'lobby_name': 'test-get-hand'})
            websocket.receive_json()
            websocket.receive_json()
            
            websocket.send_json({'action': 'lobby_start_match', 'player_name': 'host', 'lobby_name': 'test-get-hand'})
            websocket.receive_json()
            websocket.receive_json()

            websocket.send_json({'action': 'match_get_hand', 'player_name': 'host', 'match_name': 'test-get-hand'})
            data = websocket.receive_json()

            self.assertEqual(data['action'], 'get_hand')
            self.assertEqual(len(data['hand']), 9)


    def test_use_witch(self):
        with self.client.websocket_connect('/ws') as websocket:
            websocket.send_json({'action': 'lobby_create', 'player_name': 'host', 'lobby_name': 'test-use-witch'})
            websocket.receive_json()

            websocket.send_json({'action': 'lobby_join', 'player_name': 'test-player', 'lobby_name': 'test-use-witch'})
            websocket.receive_json()
            websocket.receive_json()
            
            websocket.send_json({'action': 'lobby_start_match', 'player_name': 'host', 'lobby_name': 'test-use-witch'})
            websocket.receive_json()
            websocket.receive_json()
            
            match = matchservice.get_match_by_name("test-use-witch")
            
            # host use salem witch or fail trying
            if match.player_has_witch("host"):
                websocket.send_json({'action': 'match_use_witch', 'player_name': 'host',
                                    'match_name': 'test-use-witch', 'card_type': "MONSTER"})
                data = websocket.receive_json()
                self.assertEqual(data['card']['type'], "MONSTER")
            else:
                websocket.send_json({'action': 'match_use_witch', 'player_name': 'host',
                                    'match_name': 'test-use-witch', 'card_type': "MONSTER"})
                data = websocket.receive_json()
                self.assertEqual(data['action'], "failed")

    def test_use_witch_twice(self):
        with self.client.websocket_connect('/ws') as websocket:
            websocket.send_json({'action': 'lobby_create', 'player_name': 'host', 'lobby_name': 'test-use-witch-twice'})
            websocket.receive_json()

            websocket.send_json({'action': 'lobby_join', 'player_name': 'test-player', 'lobby_name': 'test-use-witch-twice'})
            websocket.receive_json()
            websocket.receive_json()
            
            websocket.send_json({'action': 'lobby_start_match', 'player_name': 'host', 'lobby_name': 'test-use-witch-twice'})
            websocket.receive_json()
            websocket.receive_json()
            
            match = matchservice.get_match_by_name("test-use-witch-twice")
            
            if match.player_has_witch("host"):
                websocket.send_json({'action': 'match_use_witch', 'player_name': 'host',
                                    'match_name': 'test-use-witch-twice', 'card_type': "MONSTER"})
                data = websocket.receive_json()
                self.assertEqual(data['card']['type'], "MONSTER")

                websocket.send_json({'action': 'match_use_witch', 'player_name': 'host',
                                    'match_name': 'test-use-witch-twice', 'card_type': "MONSTER"})
                data = websocket.receive_json()
                self.assertEqual(data['action'], "failed")    
            elif match.player_has_witch("test-player"):
                websocket.send_json({'action': 'match_use_witch', 'player_name': 'test-player',
                                    'match_name': 'test-use-witch-twice', 'card_type': "MONSTER"})
                data = websocket.receive_json()
                self.assertEqual(data['card']['type'], "MONSTER")

                websocket.send_json({'action': 'match_use_witch', 'player_name': 'test-player',
                                    'match_name': 'test-use-witch-twice', 'card_type': "MONSTER"})
                data = websocket.receive_json()
                self.assertEqual(data['action'], "failed")

    def test_no_player_use_witch(self):
        with self.client.websocket_connect('/ws') as websocket:
            websocket.send_json({'action': 'lobby_create', 'player_name': 'host', 'lobby_name': 'test-no-player'})
            websocket.receive_json()

            websocket.send_json({'action': 'lobby_join', 'player_name': 'test-player', 'lobby_name': 'test-no-player'})
            websocket.receive_json()
            websocket.receive_json()
            
            websocket.send_json({'action': 'lobby_start_match', 'player_name': 'host', 'lobby_name': 'test-no-player'})
            websocket.receive_json()
            websocket.receive_json()

            websocket.send_json({'action': 'match_use_witch', 'player_name': 'no-player',
                                'match_name': 'test-no-player', 'card_type': "MONSTER"})
            data = websocket.receive_json()
            self.assertEqual(data['action'], "failed")

    def test_accuse_victory(self):
        with self.client.websocket_connect('/ws') as websocket:
            websocket.send_json({'action': 'lobby_create', 'player_name': 'host', 'lobby_name': 'test-accuse-victory'})
            websocket.receive_json()
            with self.client.websocket_connect('/ws') as websocket2:
                websocket2.send_json({'action': 'lobby_join', 'player_name': 'test-player-victory', 'lobby_name': 'test-accuse-victory'})
                websocket2.receive_json()
                websocket.receive_json()
                websocket.send_json({'action': 'lobby_start_match', 'player_name': 'host', 'lobby_name': 'test-accuse-victory'})
                websocket.receive_json()
                websocket2.receive_json()

                match = matchservice.get_match_by_name('test-accuse-victory')
                turn_player = match.current_turn()
                mystery = match.mystery
                if turn_player.nickname == 'host':
                    websocket.send_json({'action': 'match_accuse', 'match_name': 'test-accuse-victory', 
                                                    'monster': mystery[0].name, 'victim': mystery[1].name, 'room': mystery[2].name})
                    data = websocket.receive_json()
                else: 
                    websocket2.send_json({'action': 'match_accuse', 'match_name': 'test-accuse-victory', 
                                                    'monster': mystery[0].name, 'victim': mystery[1].name, 'room': mystery[2].name})
                    data = websocket2.receive_json()
                
                self.assertEqual(data, {'action': 'game_over', 'winner': turn_player.nickname})

    def test_accuse_defeat(self):
        with self.client.websocket_connect('/ws') as websocket:
            websocket.send_json({'action': 'lobby_create', 'player_name': 'host', 'lobby_name': 'test-accuse-defeat'})
            websocket.receive_json()
            with self.client.websocket_connect('/ws') as websocket2:
                websocket2.send_json({'action': 'lobby_join', 'player_name': 'test-player-defeat', 'lobby_name': 'test-accuse-defeat'})
                websocket2.receive_json()
                websocket.receive_json()
                websocket.send_json({'action': 'lobby_start_match', 'player_name': 'host', 'lobby_name': 'test-accuse-defeat'})
                websocket.receive_json()
                websocket2.receive_json()

                match = matchservice.get_match_by_name('test-accuse-defeat')
                turn_player = match.current_turn()
                not_turn_player = next(p for p in match.playersOnline if p.nickname != turn_player.nickname)
                mystery = match.mystery
                if turn_player.nickname == 'host':
                    websocket.send_json({'action': 'match_accuse', 'match_name': 'test-accuse-defeat', 
                                                    'monster': 'ghost', 'victim': 'conde', 'room': 'pantheon'})
                else: 
                    websocket2.send_json({'action': 'match_accuse', 'match_name': 'test-accuse-defeat', 
                                                    'monster': 'ghost', 'victim': 'conde', 'room': 'pantheon'})
                data = websocket.receive_json()
                data2 = websocket2.receive_json()
                self.assertEqual(data, {'action': 'player_deleted', 'loser': turn_player.nickname,
                                        'next_turn': not_turn_player.nickname})
                self.assertEqual(data2, {'action': 'player_deleted', 'loser': turn_player.nickname,
                                         'next_turn': not_turn_player.nickname})

    def test_accuse_no_turn(self):
        with self.client.websocket_connect('/ws') as websocket:
            websocket.send_json({'action': 'lobby_create', 'player_name': 'host', 'lobby_name': 'test-accuse-accuse-no-host'})
            websocket.receive_json()
            with self.client.websocket_connect('/ws') as websocket2:
                websocket2.send_json({'action': 'lobby_join', 'player_name': 'test-player-no-turn', 'lobby_name': 'test-accuse-accuse-no-host'})
                websocket2.receive_json()
                websocket.receive_json()
                websocket.send_json({'action': 'lobby_start_match', 'player_name': 'host', 'lobby_name': 'test-accuse-accuse-no-host'})
                websocket.receive_json()
                websocket2.receive_json()

                match = matchservice.get_match_by_name('test-accuse-accuse-no-host')
                turn_player = match.current_turn()
                if not turn_player.nickname == 'host':
                    websocket.send_json({'action': 'match_accuse', 'match_name': 'test-accuse-accuse-no-host', 
                                                    'monster': 'ghost', 'victim': 'conde', 'room': 'pantheon'})

                    data = websocket.receive_json()
                else: 
                    websocket2.send_json({'action': 'match_accuse', 'match_name': 'test-accuse-accuse-no-host', 
                                                    'monster': 'ghost', 'victim': 'conde', 'room': 'pantheon'})
                    data = websocket2.receive_json()
                
                self.assertEqual(data, {'action': 'failed', 'info': "It's not your turn"})

    def test_suspect_no_room(self):
        with self.client.websocket_connect('/ws') as websocket0:
            websocket0.send_json({'action': 'lobby_create', 'player_name': 'host', 'lobby_name': 'test-suspect-no-room'})
            websocket0.receive_json()

            with self.client.websocket_connect('/ws') as websocket1:
                websocket1.send_json({'action': 'lobby_join', 'player_name': 'test-player0', 'lobby_name': 'test-suspect-no-room'})
                websocket0.receive_json()
                websocket1.receive_json()

                websocket0.send_json({'action': 'lobby_start_match', 'player_name': 'host', 'lobby_name': 'test-suspect-no-room'})
                websocket0.receive_json()
                websocket1.receive_json()

                match = matchservice.get_match_by_name('test-suspect-no-room')

                if match.players[0].nickname == 'host':
                    websocket0.send_json({'action': 'match_suspect', 'player_name': 'host', 
                                        'match_name': 'test-suspect-no-room', 'monster': 'Dracula',
                                        'victim': 'Count', 'room': 'Bedroom'})
                    data = websocket0.receive_json()
                else:
                    websocket1.send_json({'action': 'match_suspect', 'player_name': 'test-player0', 
                                        'match_name': 'test-suspect-no-room', 'monster': 'Dracula',
                                        'victim': 'Count', 'room': 'Bedroom'})
                    data = websocket1.receive_json()

                self.assertEqual(data, {'action':'failed',
                                        'info':'You must be in a room to suspect'})
    
    def test_suspect_neg(self):
        with self.client.websocket_connect('/ws') as websocket0:
            websocket0.send_json({'action': 'lobby_create', 'player_name': 'host', 'lobby_name': 'test-suspect-neg'})
            websocket0.receive_json()

            with self.client.websocket_connect('/ws') as websocket1:
                websocket1.send_json({'action': 'lobby_join', 'player_name': 'test-player0', 'lobby_name': 'test-suspect-neg'})
                websocket0.receive_json()
                websocket1.receive_json()

                websocket0.send_json({'action': 'lobby_start_match', 'player_name': 'host', 'lobby_name': 'test-suspect-neg'})
                websocket0.receive_json()
                websocket1.receive_json()

                match = matchservice.get_match_by_name('test-suspect-neg')
                match._rolled_dice = True
                match._current_roll = 9
                match.move(Vector2d(3,6))

                if match.players[0].nickname == 'host':
                    websocket0.send_json({'action': 'match_suspect', 'player_name': 'host', 
                                        'match_name': 'test-suspect-neg', 'monster': 'Dracula',
                                        'victim': 'Count', 'room': 'Living'})
                    data1 = websocket1.receive_json()
                    self.assertEqual(data1['action'], 'question')

                    websocket1.send_json({'action': 'match_question_res', 'response': 'negative',
                                        'player_name': 'test-player0', 'reply_to': data1['reply_to'],
                                        'match_name': 'test-suspect-neg', 'monster': 'Dracula',
                                        'victim': 'Count', 'room': 'Living'})

                    res = websocket0.receive_json()
                else:
                    websocket1.send_json({'action': 'match_suspect', 'player_name': 'test-player0', 
                                        'match_name': 'test-suspect-neg', 'monster': 'Dracula',
                                        'victim': 'Count', 'room': 'Living'})
                    data0 = websocket0.receive_json()
                    self.assertEqual(data0['action'], 'question')
                    websocket0.send_json({'action': 'match_question_res', 'response': 'negative',
                                        'player_name': 'host', 'reply_to': data0['reply_to'],
                                        'match_name': 'test-suspect-neg', 'monster': 'Dracula',
                                        'victim': 'Count', 'room': 'Living'})
                    res = websocket1.receive_json()
                
                self.assertEqual(res, {'action': 'suspect_response', 'card': None})

    def test_suspect_aff(self):
        with self.client.websocket_connect('/ws') as websocket0:
            websocket0.send_json({'action': 'lobby_create', 'player_name': 'host', 'lobby_name': 'test-suspect-aff'})
            websocket0.receive_json()

            with self.client.websocket_connect('/ws') as websocket1:
                websocket1.send_json({'action': 'lobby_join', 'player_name': 'test-player0', 'lobby_name': 'test-suspect-aff'})
                websocket0.receive_json()
                websocket1.receive_json()

                websocket0.send_json({'action': 'lobby_start_match', 'player_name': 'host', 'lobby_name': 'test-suspect-aff'})
                websocket0.receive_json()
                websocket1.receive_json()

                match = matchservice.get_match_by_name('test-suspect-aff')
                match._rolled_dice = True
                match._current_roll = 9
                match.move(Vector2d(3,6))

                if match.players[0].nickname == 'host':
                    websocket0.send_json({'action': 'match_suspect', 'player_name': 'host', 
                                        'match_name': 'test-suspect-aff', 'monster': 'Dracula',
                                        'victim': 'Count', 'room': 'Living'})
                    data1 = websocket1.receive_json()
                    self.assertEqual(data1['action'], 'question')

                    websocket1.send_json({'action': 'match_question_res', 'response': 'affirmative',
                                        'player_name': 'test-player0', 'reply_to': data1['reply_to'],
                                        'match_name': 'test-suspect-aff', 'reply_card': 'Dracula'})
                    res = websocket0.receive_json()
                else:
                    websocket1.send_json({'action': 'match_suspect', 'player_name': 'test-player0', 
                                        'match_name': 'test-suspect-aff', 'monster': 'Dracula',
                                        'victim': 'Count', 'room': 'Living'})
                    data0 = websocket0.receive_json()
                    self.assertEqual(data0['action'], 'question')

                    websocket0.send_json({'action': 'match_question_res', 'response': 'affirmative',
                                        'player_name': 'host', 'reply_to': data0['reply_to'],
                                        'match_name': 'test-suspect-aff', 'reply_card': 'Dracula'})
                    res = websocket1.receive_json()
                    
                self.assertEqual(res, {'action': 'suspect_response', 'card': 'Dracula'})

    def test_match_leave(self):
        with self.client.websocket_connect('/ws') as websocket0:
            websocket0.send_json({'action': 'lobby_create', 'player_name': 'host', 'lobby_name': 'test-match-leave'})
            websocket0.receive_json()
            with self.client.websocket_connect('/ws') as websocket1:
                websocket1.send_json({'action': 'lobby_join', 'player_name': 'test-player', 'lobby_name': 'test-match-leave'})
                websocket0.receive_json()
                websocket1.receive_json()

                websocket0.send_json({'action': 'lobby_start_match', 'player_name': 'host', 'lobby_name': 'test-match-leave'})
                websocket0.receive_json()
                websocket1.receive_json()

                websocket1.send_json({'action': 'match_leave', 'player_name': 'test-player', 'match_name': 'test-match-leave'})
                dataLeft = websocket1.receive_json()
                dataKeep = websocket0.receive_json()

                self.assertEqual({dataKeep['action'],dataKeep['player']},{'player_left_match', 'test-player'})
                self.assertEqual(dataLeft['action'], 'match_leaved')

    def test_match_leave_empty(self):
        with self.client.websocket_connect('/ws') as websocket0:
            websocket0.send_json({'action': 'lobby_create', 'player_name': 'host', 'lobby_name': 'test-match-leave-empty'})
            websocket0.receive_json()
            with self.client.websocket_connect('/ws') as websocket1:
                websocket1.send_json({'action': 'lobby_join', 'player_name': 'test-player', 'lobby_name': 'test-match-leave-empty'})
                websocket0.receive_json()
                websocket1.receive_json()

                websocket0.send_json({'action': 'lobby_start_match', 'player_name': 'host', 'lobby_name': 'test-match-leave-empty'})
                websocket0.receive_json()
                websocket1.receive_json()

                websocket1.send_json({'action': 'match_leave', 'player_name': 'test-player', 'match_name': 'test-match-leave-empty'})
                websocket1.receive_json()
                websocket0.receive_json()

                websocket0.send_json({'action': 'match_leave', 'player_name': 'host', 'match_name': 'test-match-leave-empty'})
                data = websocket0.receive_json()

                self.assertEqual(data,{'action': 'match_deleted', 'info': 'no more players'})

    def test_match_leave_3_players(self):
        with self.client.websocket_connect('/ws') as websocket0:
            websocket0.send_json({'action': 'lobby_create', 'player_name': 'host', 'lobby_name': 'test-match-leave-3'})
            websocket0.receive_json()
            with self.client.websocket_connect('/ws') as websocket1:
                websocket1.send_json({'action': 'lobby_join', 'player_name': 'test-player', 'lobby_name': 'test-match-leave-3'})
                websocket0.receive_json()
                websocket1.receive_json()
                with self.client.websocket_connect('/ws') as websocket2:
                    websocket2.send_json({'action': 'lobby_join', 'player_name': 'test-player2', 'lobby_name': 'test-match-leave-3'})
                    websocket0.receive_json()
                    websocket1.receive_json()
                    websocket2.receive_json()

                    websocket0.send_json({'action': 'lobby_start_match', 'player_name': 'host', 'lobby_name': 'test-match-leave-3'})
                    websocket0.receive_json()
                    websocket1.receive_json()
                    websocket2.receive_json()

                    websocket1.send_json({'action': 'match_leave', 'player_name': 'test-player', 'match_name': 'test-match-leave-3'})
                    dataLeft = websocket1.receive_json()
                    dataKeep1 = websocket0.receive_json()
                    dataKeep2 = websocket2.receive_json()

                    self.assertEqual({dataKeep1['action'],dataKeep1['player']},{'player_left_match', 'test-player'})
                    self.assertEqual(dataKeep2,{'action': 'player_left_match', 'player': 'test-player', 'hand': dataKeep1['hand']})
                    self.assertEqual(dataLeft['action'], 'match_leaved')