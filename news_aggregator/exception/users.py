# -*- encoding:utf-8 -*-
"""
                                                  - File description -
------------------------------------------------------------------------------------------------------------------------
Exceptions related to users logic.
"""
from exception.base import BaseAppException


class UserNotFound(BaseAppException):
    exception_code = "U-DATA-NOT-FOUND"

    _default_error_message = "No user data was found"


class EmailAlreadyInUse(BaseAppException):
    exception_code = "U-EMAIL-IN-USE"

    _default_error_message = "The email is already registered in the system. Did you forget your password?"


# TODO: Incluir una comprobación transversal en cualquier procesador para que compruebe esta condición antes de consumir
#  cualquier recurso.
class UserAccountDeactivated(BaseAppException):
    exception_code = "U-ACC-DEACTIVATED"

    _default_error_message = "The account of the given user is deactivated. Activate it first to operate"


class UserAlreadySubscribed(BaseAppException):
    exception_code = "U-ALREADY-SUBSCRIBED"

    _default_error_message = "The user is already subscribed to the provided RSS feed"


class UserHasNoSubscriptions(BaseAppException):
    exception_code = "U-NO-SUBSCRIPTIONS"

    _default_error_message = "The given user has no subscriptions"


class NoNewUserDataProvided(BaseAppException):
    exception_code = "U-NO-NEW-DATA-PROVIDED"

    _default_error_message = "No new user data was provided"

    def __init__(self, *args, **kwargs):
        super(NoNewUserDataProvided, self).__init__(*args, **kwargs)
        self._http_status_code = 400


class IncorrectPassword(BaseAppException):
    exception_code = "U-INCORRECT-PASSWORD"

    _default_error_message = "The provided password is incorrect"
