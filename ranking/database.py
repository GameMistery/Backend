from pony.orm import *

db = Database()

class Ranking(db.Entity):
    user_name = PrimaryKey(str, auto=False)
    victories = Required(int)

db.bind(provider= 'sqlite', filename= 'Misterio.sqlite', create_db= True)
db.generate_mapping(create_tables= True)