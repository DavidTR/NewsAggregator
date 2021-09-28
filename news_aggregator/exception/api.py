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

    def __init__(self, *args, **kwargs):
        super(BaseAPIException, self).__init__(*args, **kwargs)
        self._http_status_code = 400


class MissingQueryStringArguments(BaseAPIException):
    exception_code = "API-QS-ARGS-MISSING"

    _default_error_message = "No querystring arguments found"


class MissingBodyArguments(BaseAPIException):
    exception_code = "API-BODY-ARGS-MISSING"

    _default_error_message = "No body arguments found"


class UnableToParseArguments(BaseAPIException):
    exception_code = "API-ARGS-PARSE"

    _default_error_message = "Unable to parse the given arguments"

    def __init__(self, *args, **kwargs):
        super(UnableToParseArguments, self).__init__(*args, **kwargs)
        self._http_status_code = 400
        self._recommendation_message = "Please check your request arguments and try again"
