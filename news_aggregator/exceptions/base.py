# -*- encoding:utf-8 -*-
"""
                                                  - File description -
------------------------------------------------------------------------------------------------------------------------
Base exception classes.
"""


class AppException(Exception):

    # All exceptions will have an unique alphanumeric code.
    exception_code = ""
    _default_error_message = "An error occurred, please try again"

    # List that contains the exception codes of all the exception classes. Used to control that every exception class
    # has an unique exception code.
    _exception_code_registry = []

    def __init__(self, error_message: str):
        super(AppException, self).__init__()
        self._error_message = error_message or self._default_error_message

    def __init_subclass__(cls, **kwargs):
        """Enforces the uniqueness of exception_code for every exception subclass"""
        super(AppException, cls).__init_subclass__(**kwargs)
        exception_code = getattr(cls, 'exception_code')
        if not exception_code or (exception_code and exception_code in cls._exception_code_registry):
            raise RuntimeError(f"The exception class {cls.__name__} has an already used exception code")

        cls._exception_code_registry.append(exception_code)

    @property
    def error_message(self) -> str:
        return self._error_message

    def __str__(self) -> str:
        """
        Return a string representation of the error. The error message will be formatted with the data held in the
        instance
        """
        return f"An error occurred: {self._error_message}"

    def __repr__(self) -> str:
        """Returns a string representation of the instance that can be used to re-create it"""
        return f"{self.__class__.__name__}(\"{self.error_message}\")"
