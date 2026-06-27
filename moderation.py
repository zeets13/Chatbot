from database import *

from datetime import datetime, timedelta
from config import MAX_VIOLATIONS
from config import BLOCK_TIME_MINUTES

def is_user_blocked(username):

    create_user(username)

    user = get_user(username)

    if user["blocked_until"] is None:

        return False, None

    blocked_until = datetime.fromisoformat(user["blocked_until"])

    if datetime.now() >= blocked_until:

        update_block(username, None)

        return False, None

    remaining = blocked_until - datetime.now()

    return True, remaining

def add_violation(username):

    create_user(username)

    user = get_user(username)

    violations = user["violations"] + 1

    update_violations(username, violations)

    return violations

def reset_violations(username):

    update_violations(username, 0)

def block_user(username):

    blocked_until = datetime.now() + timedelta(BLOCK_TIME_MINUTES)

    update_block(
        username,
        blocked_until.isoformat()
    )

    return blocked_until
def process_violation(username):

    violations = add_violation(username)

    if violations >= MAX_VIOLATIONS:

        block_user(username)

        return {

            "blocked": True,

            "violations": violations

        }

    return {

        "blocked": False,

        "violations": violations

    }
