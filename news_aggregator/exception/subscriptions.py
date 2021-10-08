# -*- encoding:utf-8 -*-
"""
                                                  - File description -
------------------------------------------------------------------------------------------------------------------------

"""
from exception.base import BaseAppException


class SubscriptionDoesNotExist(BaseAppException):
    exception_code = "SUBS-DOES-NOT-EXIST"

    _default_error_message = "The user is not subscribed to the given RSS feed"
