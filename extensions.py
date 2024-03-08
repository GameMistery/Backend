"""
Global instances of services and dependencies
"""

from lobby.lobby_service import LobbyService
from matches.match_service import MatchService

lobbyservice = LobbyService()
matchservice = MatchService()