from collections import deque
from typing import List
from users.user import User
from .match import Match
from .entities.deck import Deck
from .entities.card import Card


class MatchService:

    def __init__(self):
        self.matches = []

    def create_new_match(self, name: str, players: List[User], chat:deque) -> Match:
        match = Match(name, players, chat)
        self.matches.append(match)

        deck = Deck(match)
        deck.deal_cards()

        return match

    def get_matches(self) -> List[Match]:
        return self.matches

    def get_match_by_name(self, name) -> Match:
        return next(m for m in self.matches if m.name == name)

    def get_player_in_match(self, match: Match, player: str):
        return next(start_player for start_player in match.players if start_player.nickname == player)

    def delete_match(self, match: Match):
        match.players = []
        match.playersOnline = []
        self.matches.remove(match)

    def delete_player(self, match: Match, player: User):
        match.players.remove(player)

    def offline_player(self, match: Match, player: User):
        match.playersOnline.remove(player)

    def hand_text(self, hand: List[Card]) -> List[str]:
        textHand = []
        for card in hand:
            textHand.append(card.name)
        return textHand
