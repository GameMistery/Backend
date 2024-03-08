from pony.orm import *
from users.user import User
from ranking.database import Ranking

@db_session
def db_get_top_ten():
    top_ten = []
    i = 0
    for player in Ranking.select().order_by(desc(Ranking.victories)):
        if (i>=10):
            break
        top_ten.append({'player': player.user_name,'victories': player.victories})
        i += 1
    return top_ten

@db_session
def db_add_record(player: User) -> None:
    if (Ranking.exists(lambda p: p.user_name == player.nickname)):
        Ranking[player.nickname].victories += 1
    else:
        Ranking(user_name= player.nickname, victories= 1)