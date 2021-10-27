# -*- encoding:utf-8 -*-
"""
                                                  - File description -
------------------------------------------------------------------------------------------------------------------------

"""
import re

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


def decode_and_clean_xml_data(xml_data: bytes) -> str:
    """Decode and clean an XML bytes sequence, returning it as an UTF-8 decoded string"""

    # The response is decoded as an UTF-8 string to avoid encoding errors in the database and to be
    # displayed correctly in the service's response. Clear special and unnecessary characters that would
    # add to the XML's length.
    clean_pattern = r"[\t\n]"
    xml_utf_string = re.sub(clean_pattern, '', xml_data.decode('utf-8'))

    # Also, substitute non-standard quotation marks (“”) for the standard ones (""), as they could be a source of
    # encoding problems.
    double_quotes_pattern = r"[“”]"
    xml_utf_string = re.sub(double_quotes_pattern, '"', xml_utf_string)

    return xml_utf_string
