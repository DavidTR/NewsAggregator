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


class ParametersNotSet(ValidationException):
    """This exception will be risen if the parameters have not been set and the service tries to validate them"""
    exception_code = "VAL-PARAMS-NOT-SET"
