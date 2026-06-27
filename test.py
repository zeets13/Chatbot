from database import *

initialize_database()

create_user("Jarifa")

user = get_user("Jarifa")

print(dict(user))