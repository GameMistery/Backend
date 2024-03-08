class User:

    def __init__(self, nickname: str):
        self.nickname = nickname

    def __eq__(self, other):
        return self.nickname == other.nickname
