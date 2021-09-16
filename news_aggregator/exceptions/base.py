# -*- encoding:utf-8 -*-
"""
                                                  - File description -
------------------------------------------------------------------------------------------------------------------------

"""


class AppException(Exception):

    def __init__(self, error_message: str, formatting_data: dict):
        super(AppException, self).__init__()

        self._error_message = error_message
        self._formatting_data = formatting_data or {}

    def __str__(self):
        """Emit a string representation of the error. The error message will be formatted with the data held in """
        return f"A controlled error occurred: {self._error_message.format(**self._formatting_data)}"

    def __repr__(self):
        pass
