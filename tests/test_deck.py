import unittest
from matches.entities.deck import Deck
from matches.match import Match
from users.user import User

class TestDeck(unittest.TestCase):

    def test_six_players_match(self):
        match = Match("Test-deck0", [User("Player0"), User("Player1"), User("Player2"),
                                    User("Player3"), User("Player4"), User("Player5")])
        deck = Deck(match)

        deck.deal_cards()

        # Since there are six players and 18 cards, each one receives 3 cards
        for i in range(0,6):
            self.assertEqual(len(match.cards[i]), 3)

    def test_four_players_match(self):
        match = Match("Test-deck0", [User("Player0"), User("Player1"), User("Player2"), User("Player3")])
        deck = Deck(match)

        deck.deal_cards()

        # As there are four players and 18 cards, two players receive 5
        # cards and the other two only 4
        for i in range(0,2):
            self.assertEqual(len(match.cards[i]), 5)
        for i in range(2,4):
            self.assertEqual(len(match.cards[i]), 4)    
