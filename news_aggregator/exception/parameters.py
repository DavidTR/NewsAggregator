# -*- encoding:utf-8 -*-
"""
                                                  - File description -
------------------------------------------------------------------------------------------------------------------------
Parameter related exceptions
"""
from exception.base import BaseAppException


class InvalidParameterType(BaseAppException):
    """This exception will be risen when a parameter has an invalid type"""
    exception_code = "P-TYPE"

    _default_error_message = "The parameter (parameter_name)s is of an invalid type"


class IncorrectParameterFormat(BaseAppException):
    """This exception will be risen when a parameter has an invalid format"""
    exception_code = "P-FORMAT"

    _default_error_message = "The parameter (parameter_name)s has an incorrect format"
