# -*- encoding:utf-8 -*-
"""
                                                  - File description -
------------------------------------------------------------------------------------------------------------------------

"""
from exception.base import BaseAppException


class AliveSessionAlreadyExists(BaseAppException):
    exception_code = "S-ALIVE-SESSION-EXISTS"

    _default_error_message = "An alive session already exists"


class SessionDoesNotExist(BaseAppException):
    exception_code = "S-DOES-NOT-EXIST"

    _default_error_message = "The session does not exist or it does not belong to the given user"


class SessionIsNotAlive(BaseAppException):
    exception_code = "S-IS-NOT-ALIVE"

    _default_error_message = "The session is expired or closed"

    def __init__(self, *args, **kwargs):
        super(SessionIsNotAlive, self).__init__(*args, **kwargs)
        self._http_status_code = 400

