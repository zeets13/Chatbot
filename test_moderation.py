from moderation import *

initialize_database()

username = "Jarifa"

print(process_violation(username))

print(process_violation(username))

print(process_violation(username))

blocked, remaining = is_user_blocked(username)

print(blocked)

print(remaining)