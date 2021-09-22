# -*- encoding:utf-8 -*-
"""
                                                  - File description -
------------------------------------------------------------------------------------------------------------------------

"""
import re


def is_email_valid(email: str) -> bool:
    """Checks if the given email is valid"""
    email_regex = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")

    # "fullmatch" checks if the whole string matches the regular expression.
    if not isinstance(email, str) or not email_regex.fullmatch(email):
        return False

    return True
