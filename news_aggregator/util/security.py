# -*- encoding:utf-8 -*-
"""
                                                  - File description -
------------------------------------------------------------------------------------------------------------------------
Does not have enough weight to be a package

To tune up bcrypt, see:
    - https://security.stackexchange.com/questions/3959/recommended-of-iterations-when-using-pbkdf2-sha256/3993#3993
"""
import time
import uuid
from base64 import urlsafe_b64encode
from math import trunc

import bcrypt


def hash_password(password: str) -> bytes:
    """Hashes a plain password"""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('UTF-8'), salt)


def check_password(password: str, hashed_password: str) -> bool:
    """Checks if the given password was used to create hashed_password"""
    return bcrypt.checkpw(password.encode('UTF-8'), hashed_password.encode('UTF-8'))


def create_session_id(user_id: int) -> str:
    """Creates a session ID that will be related to an user ID"""

    # The session ID needs to be secure in order to prevent malicious agents to generate session IDs and create fake
    # cookies with them, compromising user accounts.
    timestamp = trunc(time.time())
    salt = f"{user_id}-{timestamp}"
    random_uuid_hex = uuid.uuid4().hex
    salt_and_uuid = salt + random_uuid_hex

    session_id = urlsafe_b64encode(salt_and_uuid.encode()).decode()

    return session_id
