import unittest
from matches.match import Match
from users.user import User
from matches.entities.deck import Deck

class TestMatch2Players(unittest.TestCase):

    def setUp(self) -> None:
        self.match = Match('testmatch', [User("host"), User("user1")])

    def test_correct_turns(self):
        turns = self.match.players

        self.match.roll_dice()
        self.match.move(self.match.board.get_player_position(turns[0].nickname))
        self.assertTrue(turns[1] == self.match.next_turn(),
            "The next turn doesn't belong to the correct user")

        self.match.roll_dice()
        self.match.move(self.match.board.get_player_position(turns[1].nickname))
        self.assertTrue(turns[0] == self.match.next_turn(),
            "The next turn doesn't belong to the correct user")


class TestMatch6Players(unittest.TestCase):

    def setUp(self) -> None:
        self.match = Match('testmatch', [User("host"), User("user1"),
                                        User("user2"), User("user3"),
                                        User("user4"), User("user5"),])
        deck = Deck(self.match)
        deck.deal_cards()

    def test_correct_turns(self):
        turns = self.match.players
        self.match.roll_dice()
        self.match.move(self.match.board.get_player_position(turns[0].nickname))
        self.assertTrue(turns[1] == self.match.next_turn(),
            "The next turn doesn't belong to the correct user")
        self.match.roll_dice()
        self.match.move(self.match.board.get_player_position(turns[1].nickname))
        self.assertTrue(turns[2] == self.match.next_turn(),
            "The next turn doesn't belong to the correct user")
        self.match.roll_dice()
        self.match.move(self.match.board.get_player_position(turns[2].nickname))
        self.assertTrue(turns[3] == self.match.next_turn(),
            "The next turn doesn't belong to the correct user")
        self.match.roll_dice()
        self.match.move(self.match.board.get_player_position(turns[3].nickname))
        self.assertTrue(turns[4] == self.match.next_turn(),
            "The next turn doesn't belong to the correct user")
        self.match.roll_dice()
        self.match.move(self.match.board.get_player_position(turns[4].nickname))
        self.assertTrue(turns[5] == self.match.next_turn(),
            "The next turn doesn't belong to the correct user")
        self.match.roll_dice()
        self.match.move(self.match.board.get_player_position(turns[5].nickname))
        self.assertTrue(turns[0] == self.match.next_turn(),
            "The next turn doesn't belong to the correct user")

    def test_get_hand(self):
        try:
            hand = self.match.get_hand("user3")
            self.assertEqual(len(hand), 3)
        except Exception:
            self.assertTrue(False)        

    def test_get_hand_for_no_player(self):
        try:
            self.match.get_hand("user6")
            self.assertTrue(False, 
                "Get hand of a non existent player didn't raise an exception")
        except Exception:
            self.assertTrue(True)