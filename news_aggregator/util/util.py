# -*- encoding:utf-8 -*-
"""
                                                  - File description -
------------------------------------------------------------------------------------------------------------------------

"""
from cfg import config
from const.data import EXECUTION_MODES


def fast_list_flattener(list_of_lists: list) -> list:
    """
    Since the += operator is quite well optimized, this is one of the fastest ways to flatten a list.
    See: https://chrisconlan.com/fastest-way-to-flatten-a-list-in-python/
    """
    result = []
    for _list in list_of_lists:
        result += _list
    return result


def get_session_expiration_delay() -> int:
    """Returns the session expiration delay (in minutes), depending on the app's execution mode"""

    if config.settings.EXECUTION_MODE == EXECUTION_MODES["prod"]:
        session_expiration_delay = 5
    elif config.settings.EXECUTION_MODE == EXECUTION_MODES["dev"]:
        session_expiration_delay = 1440
    else:
        session_expiration_delay = 10

    return session_expiration_delay
