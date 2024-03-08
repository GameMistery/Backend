from typing import List
from users.user import User
from .lobby import Lobby


class LobbyService:

    def __init__(self):
        self.lobbies = []

    def create_new_lobby(self, lobby_name: str, host: User) -> Lobby:
        if not isinstance(host, User):
            raise Exception('Host should be of type User')

        # Defaults to player's nickname if no lobby name is provided
        if lobby_name is None or lobby_name == '':
            lobby_name = f"{host.nickname}'s lobby"

        for lobby in self.lobbies:
            if lobby.name == lobby_name:
                raise Exception('Duplicate lobby name')

        lobby = Lobby(lobby_name, host)
        self.lobbies.append(lobby)
        return lobby

    def get_lobbies(self) -> List[Lobby]:
        return self.lobbies

    def get_lobby_by_name(self, name: str) -> Lobby:
        return next(lobby for lobby in self.lobbies if lobby.name == name)

    def join_player(self, lobby_name: str, player: User) -> None:
        if not isinstance(player, User):
            raise Exception('Player should be of type User')
        
        lobby = self.get_lobby_by_name(lobby_name)

        if player in lobby.players:
            raise Exception('Duplicate player name')

        lobby.join(player)

    def get_player_in_lobby(self, lobby: Lobby, player: str):
        return next(start_player for start_player in lobby.players if start_player.nickname == player)

    def delete_lobby(self, lobby: Lobby):
        for player in lobby.players:
            lobby.players.remove(player)
        self.lobbies.remove(lobby)