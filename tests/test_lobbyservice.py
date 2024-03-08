import unittest 
from lobby.lobby_service import LobbyService
from lobby.lobby import Lobby
from users.user import User


class TestLobbyService(unittest.TestCase):

    def setUp(self) -> None:
        self.lobby_service = LobbyService()

    def test_create_lobby(self):
        self.lobby_service.create_new_lobby("test-lobby", User("test-host"))

        self.assertEqual(self.lobby_service.lobbies,
                        [Lobby("test-lobby", User("test-host"))],
                        "The lobby was not created")

    def test_create_lobby_with_empty_name(self):
        self.lobby_service.create_new_lobby("", User("test-host"))

        self.assertEqual(self.lobby_service.lobbies,
                        [Lobby("test-host's lobby", User("test-host"))],
                        "The lobby was not created")

    def test_create_lobby_with_None_name(self):
        self.lobby_service.create_new_lobby(None, User("test-host"))

        self.assertEqual(self.lobby_service.lobbies,
                        [Lobby("test-host's lobby", User("test-host"))],
                        "The lobby was not created")
    
    def test_create_lobby_without_host(self):
        try:
            self.lobby_service.create_new_lobby("test-lobby", None)
            self.assertTrue(False, 'Passing None as host should raise an exception')
        except Exception:
            self.assertTrue(True)

    def test_get_lobbies(self):
        self.lobby_service.create_new_lobby("test-lobby-1", User("test-host-1"))
        self.lobby_service.create_new_lobby("test-lobby-2", User("test-host-2"))
        self.lobby_service.create_new_lobby("test-lobby-3", User("test-host-3"))

        lobbies = self.lobby_service.get_lobbies()

        self.assertEqual(lobbies, [Lobby("test-lobby-1", User("test-host-1")),
                                    Lobby("test-lobby-2", User("test-host-2")),
                                    Lobby("test-lobby-3", User("test-host-3"))],
                                    "The list of lobbies does not match the lobbies created")

    def test_join_into_non_existent_lobby(self):
        self.lobby_service.create_new_lobby("test-lobby", User("test-host"))
        try:
            self.lobby_service.join_player("test-loby", User("test-player"))
            self.assertTrue(False, 
                "Joining non-existent lobby didn't raise 'StopIteration' exception")
        except StopIteration:
            self.assertTrue(True)

    def test_create_lobby_without_player(self):
        self.lobby_service.create_new_lobby("test-lobby", User("test-host"))
        try:
            self.lobby_service.join_player("test-lobby", None)
            self.assertTrue(False, 'Passing None as host should raise an exception')
        except Exception:
            self.assertTrue(True)
        