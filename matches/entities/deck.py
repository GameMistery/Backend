import random
from matches.match import Match
from .card import Card

class Deck:

    def __init__(self, match: Match) -> None:
        self.match = match

        # Define the deck
        self.cards = [
            Card("Monster", "Dracula"), Card("Monster", "Frankenstein"), Card("Monster", "Werewolf"),
            Card("Monster", "Ghost"), Card("Monster", "Mummy"), Card("Monster", "Dr. Jekyll And Mr Hyde"),
            Card("Victim", "Count"), Card("Victim", "Countess"), Card("Victim", "Housekeeper"),
            Card("Victim", "Butler"), Card("Victim", "Maid"), Card("Victim", "Gardener"),
            Card("Room", "Bedroom"), Card("Room", "Library"), Card("Room", "Cellar"),
            Card("Room", "Garage"), Card("Room", "Laboratory"), Card("Room", "Pantheon"),
            Card("Room", "Dining"), Card("Room", "Living"), Card("Salem Witch", "Salem Witch")
        ]

        # Define the mystery
        self.match.mystery = (random.choice(self.cards[0:6]),
                              random.choice(self.cards[6:12]),
                              random.choice(self.cards[12:20]))

        for card in self.match.mystery:
            self.cards.remove(card)

        # Shuffle the deck cards
        random.shuffle(self.cards)

    def deal_cards(self) -> None:
        n_players = len(self.match.players)
        for i in range (0,18):
            self.match.cards[i%n_players].append(self.cards[i])
