# -*- encoding:utf-8 -*-
"""
                                                  - File description -
------------------------------------------------------------------------------------------------------------------------
Validation exceptions. These exceptions should be used whenever a validation needs to be performed. For example,
parameter type/format or logic conditions validations


TODO: Revisar los mensajes de excepción
"""
from exception.base import BaseAppException


class ValidationException(BaseAppException):
    """Base class for validation exceptions"""
    exception_code = "VAL"

    def __init__(self, *args, **kwargs):
        super(ValidationException, self).__init__(*args, **kwargs)

        # For validation internal exceptions will return a 422 HTTP code. It's more specific than 409 and relates more
        # to the fact that, although it was well formed, there were semantic errors in the request .
        # See:
        #   - https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/422
        #   - https://www.bennadel.com/blog/2434-http-status-codes-for-invalid-data-400-vs-422.htm
        # NOTE: If a validation exception isn't related to this scenario, it must overwrite its own constructor to
        # set a more suitable HTTP error code.
        self._http_status_code = 422


class InvalidType(ValidationException):
    """This exception will be risen when a field has an invalid type"""
    exception_code = "VAL-TYPE"

    _default_error_message = "The field has an invalid type"


class IncorrectFormat(ValidationException):
    """This exception will be risen when a field has an invalid format"""
    exception_code = "VAL-FORMAT"

    _default_error_message = "The field has an incorrect format"


class InsufficientLength(ValidationException):
    """This exception will be risen when a field does not have the minimum number of characters"""
    exception_code = "VAL-MIN-LENGTH"

    _default_error_message = "The field does not have the required minimum length"


class MaxLengthExceeded(ValidationException):
    """This exception will be risen when a field has in insufficient character length"""
    exception_code = "VAL-MAX-LENGTH"

    _default_error_message = "The field's length surpasses its maximum"


class NotEnoughCapitalLetters(ValidationException):
    """This exception will be risen when a field has in insufficient number of capital letters"""
    exception_code = "VAL-CAPITAL"

    _default_error_message = "The field does not have the required minimum amount of capital letters"


class NotEnoughSpecialCharacters(ValidationException):
    """This exception will be risen when a field has in insufficient number of special, punctuation characters"""
    exception_code = "VAL-SPECIAL"

    _default_error_message = "The field does not contain the required minimum amount of special characters"


class MissingField(ValidationException):
    """This exception will be risen when a field has not been provided"""
    exception_code = "VAL-PARAM-MISSING"

    _default_error_message = "The field has not been informed"

    def __init__(self, *args, **kwargs):
        super(ValidationException, self).__init__(*args, **kwargs)
        self._http_status_code = 400


class ParametersNotSet(ValidationException):
    """This exception will be risen if the parameters have not been set and the service tries to validate them"""
    exception_code = "VAL-PARAMS-NOT-SET"

    def __init__(self, *args, **kwargs):
        super(ValidationException, self).__init__(*args, **kwargs)
        self._http_status_code = 400


class IntegerTooLarge(ValidationException):
    """This exception will be risen if an integer reaches a maximum value"""
    exception_code = "VAL-INT-TOO-LARGE"

    _default_error_message = "The integer value is too large"

    def __init__(self, *args, **kwargs):
        super(ValidationException, self).__init__(*args, **kwargs)
        self._http_status_code = 400


class IntegerTooSmall(ValidationException):
    """This exception will be risen if an integer reaches a maximum value"""
    exception_code = "VAL-INT-TOO-SMALL"

    _default_error_message = "The integer value is too small"

    def __init__(self, *args, **kwargs):
        super(ValidationException, self).__init__(*args, **kwargs)
        self._http_status_code = 400


class InvalidListMemberDataType(ValidationException):
    exception_code = "VAL-INVALID-MEMBER-TYPE"

    _default_error_message = "A member of the list has a not allowed data type. " \
                             "Allowed data types: {allowed_data_types}"

