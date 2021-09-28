# -*- encoding:utf-8 -*-
"""
                                                  - File description -
------------------------------------------------------------------------------------------------------------------------
API package specific exceptions.

"""
from exception.base import BaseAppException


class BaseAPIException(BaseAppException):
    """Base class for API exceptions"""
    exception_code = "API"


class MissingQueryStringArguments(BaseAPIException):

    exception_code = "API-QS-ARGS-MISSING"

    _default_error_message = "No querystring arguments found"


class MissingBodyArguments(BaseAPIException):
    exception_code = "API-BODY-ARGS-MISSING"

    _default_error_message = "No body arguments found"
