# -*- encoding:utf-8 -*-
"""
                                                  - File description -
------------------------------------------------------------------------------------------------------------------------

"""


def fast_list_flattener(list_of_lists: list) -> list:
    """
    Since the += operator is quite well optimized, this is one of the fastest ways to flatten a list.
    See: https://chrisconlan.com/fastest-way-to-flatten-a-list-in-python/
    """
    result = []
    for _list in list_of_lists:
        result += _list
    return result
