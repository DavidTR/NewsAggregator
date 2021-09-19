# -*- encoding:utf-8 -*-
"""
                                                  - File description -
------------------------------------------------------------------------------------------------------------------------
Exceptions related to users logic.
"""
from exceptions.base import AppException


class UserDataNotFound(AppException):
    exception_code = "U001"
