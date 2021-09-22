# -*- encoding:utf-8 -*-
"""
                                                  - File description -
------------------------------------------------------------------------------------------------------------------------
Exceptions related to users logic.
"""
from exception.base import BaseAppException


class UserNotFound(BaseAppException):
    exception_code = "U001"

    _default_error_message = "No user data found with the provided credentials"
