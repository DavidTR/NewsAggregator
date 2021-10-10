# -*- encoding:utf-8 -*-
"""
                                                  - File description -
------------------------------------------------------------------------------------------------------------------------

"""
from exception.base import BaseAppException


class AliveSessionAlreadyExists(BaseAppException):
    exception_code = "S-ALIVE-SESSION-EXISTS"

    _default_error_message = "An alive session already exists"
