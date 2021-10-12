# -*- encoding:utf-8 -*-
"""
                                                  - File description -
------------------------------------------------------------------------------------------------------------------------

"""
from exception.base import BaseAppException


class SubscriptionDoesNotExist(BaseAppException):
    exception_code = "SUBS-DOES-NOT-EXIST"

    _default_error_message = "The user is not subscribed to the given RSS feed"


class NewOrderListIncorrectLength(BaseAppException):
    exception_code = "S-ORDER-LIST-INVALID-LENGTH"

    _default_error_message = "The new order list has an incorrect length"

    def __init__(self, *args, **kwargs):
        super(NewOrderListIncorrectLength, self).__init__(*args, **kwargs)
        self._http_status_code = 400


class MalformedNewOrderList(BaseAppException):
    exception_code = "S-MALFORMED-ORDER-LIST"

    _default_error_message = "The new order list is malformed"

    def __init__(self, *args, **kwargs):
        super(MalformedNewOrderList, self).__init__(*args, **kwargs)
        self._http_status_code = 400


class InvalidRSSFeedInNewOrderList(BaseAppException):
    exception_code = "S-INVALID-RSS-ORDER-LIST"

    _default_error_message = "There is a RSS feed ID that the user is not subscribed to in the new order list"

    def __init__(self, *args, **kwargs):
        super(InvalidRSSFeedInNewOrderList, self).__init__(*args, **kwargs)
        self._http_status_code = 400


class InvalidOrderValueInNewOrderList(BaseAppException):
    exception_code = "S-INVALID-VALUE-ORDER-LIST"

    _default_error_message = "There is an invalid order value in the new order list. " \
                             "The allowed values are: {allowed_order_values}"

    def __init__(self, *args, **kwargs):
        super(InvalidOrderValueInNewOrderList, self).__init__(*args, **kwargs)
        self._http_status_code = 400


