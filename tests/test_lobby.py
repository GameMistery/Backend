import unittest
from lobby.lobby import Lobby
from users.user import User


class TestLobby(unittest.TestCase):

    def setUp(self) -> None:
        self.lobby = Lobby('testlobby', User("host"))

    def test_join_when_full(self):
        for i in range(self.lobby.MAX_PLAYERS - 1):
            self.lobby.join(User(f'user{i}'))

        try:
            self.lobby.join(User('user6'))
            self.assertTrue(False, 
                            "Joining when lobby is full didn't raise an exception")
        except Exception:
            self.assertTrue(True)

    def test_user_cant_start(self):
        user1 = User('user1')
        self.lobby.join(user1)
        
        self.assertFalse(self.lobby.can_start(user1), 
                         "A non-host user can start a game")

    def test_host_can_start(self):
        self.lobby.join(User("user1"))
        self.lobby.join(User("user2"))
        self.lobby.join(User("user3"))

        self.assertTrue(self.lobby.can_start(self.lobby.host),
                        "The host user cannot start a valid game")

    def test_host_start_empty_lobby(self):
        self.assertFalse(self.lobby.can_start(self.lobby.host),
                         "The host user start a invalid game")

    def test_user_leaves_lobby(self):
        user1 = User("user1")
        self.lobby.join(user1)
        self.lobby.join(User("user2"))

        self.assertTrue(user1 in self.lobby.players,
            "User 1 isn't in the player list")

        self.lobby.leave(user1)

        self.assertFalse(user1 in self.lobby.players,
                         "User 1 isn't in the player list")

    def test_current_players(self):
        user1 = User("user1")
        self.lobby.join(user1)
        self.lobby.join(User("user2"))

        self.assertEqual(self.lobby.current_players(), 3,
                         "There are three players but the player counter is wrong")

        self.lobby.leave(user1)

        self.assertEqual(self.lobby.current_players(), 2, 
                         "A user left the room but the player counter isn't updated")

    def test_host_leaves_lobby(self):
        self.lobby.join(User("user1"))
        self.lobby.join(User("user2"))
        self.lobby.join(User("user3"))

        self.lobby.leave(self.lobby.host)

        self.assertEqual(self.lobby.current_players(), 0, 
                         "The host user left the room, but the other players are still in the room")
