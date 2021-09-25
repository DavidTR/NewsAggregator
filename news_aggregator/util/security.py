# -*- encoding:utf-8 -*-
"""
                                                  - File description -
------------------------------------------------------------------------------------------------------------------------
Does not have enough weight to be a package

To tune up bcrypt, see:
    - https://security.stackexchange.com/questions/3959/recommended-of-iterations-when-using-pbkdf2-sha256/3993#3993
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """Hashes a plain password"""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('UTF-8'), salt)


def check_password(password: str, hashed_password: str) -> bool:
    """Checks if the given password was used to create hashed_password"""
    return bcrypt.checkpw(password.encode('UTF-8'), hashed_password.encode('UTF-8'))
