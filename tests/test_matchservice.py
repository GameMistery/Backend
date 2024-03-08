import unittest 
from collections import deque
from matches.match_service import MatchService
from matches.match import Match
from users.user import User

class TestMatchService(unittest.TestCase):

    def setUp(self) -> None:
        self.match_service = MatchService()

    def test_create_match(self):
        self.match_service.create_new_match('test-match', [User('host'), User('Player2')], deque([], maxlen=100))
        self.assertEqual(self.match_service.matches,
                        [Match('test-match', [User('host'),User('Player2')])],
                        "The match was not created")
    
    def test_get_matches(self):
        self.assertEqual(self.match_service.get_matches(), [], 
                            "Random matches was found")

        self.match_service.create_new_match('test-match', [User('host'), User('Player2')], deque([], maxlen=100))
        self.match_service.create_new_match('test-match-b', [User('host-b'), User('Player2-b')], deque([], maxlen=100))

        match_list = self.match_service.get_matches()
        match_list_test = [Match('test-match', [User('host'), User('Player2')]),
                            Match('test-match-b', [User('host-b'), User('Player2-b')])]

        self.assertEqual(match_list, match_list_test, 
                            "The list of matches does not match the matches created")

    def test_get_match_by_name(self):
        self.match_service.create_new_match('test-match', [User('host'), User('Player2')], deque([], maxlen=100))

        self.assertEqual(self.match_service.get_match_by_name('test-match'),
                            Match('test-match', [User('host'), User('Player2')]), 
                            "The match was not found")      