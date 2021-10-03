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


class EmailAlreadyInUse(BaseAppException):
    exception_code = "U-EMAIL-IN-USE"

    _default_error_message = "The email is already registered in the system. Did you forget your password?"


# TODO: Incluir una comprobación transversal en cualquier procesador para que compruebe esta condición antes de consumir
#  cualquier recurso.
class UserAccountDeactivated(BaseAppException):
    exception_code = "U-ACC-DEACT"

    _default_error_message = "The account of the given user is deactivated. Activate it first to operate"


class UserAlreadySubscribed(BaseAppException):
    exception_code = "U-ALREADY-SUB"

    _default_error_message = "The user is already subscribed to the provided RSS feed"
