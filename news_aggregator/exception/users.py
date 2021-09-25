# -*- encoding:utf-8 -*-
"""
                                                  - File description -
------------------------------------------------------------------------------------------------------------------------
Exceptions related to users logic.
"""
from exception.base import BaseAppException


class UserNotFound(BaseAppException):
    exception_code = "U-DATA-NOT-FOUND"

    _default_error_message = "No user data found with the provided credentials"


class EmailAlreadyRegistered(BaseAppException):
    exception_code = "U-EMAIL-REG"

    _default_error_message = "The email is already registered in the system. Did you forget your password?"
