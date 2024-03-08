from .user import User


class NetworkUser(User):

    def __init__(self, nickname, socket):
        super().__init__(nickname)
        self.socket = socket

    def __eq__(self, other):
        return self.nickname == other.nickname
