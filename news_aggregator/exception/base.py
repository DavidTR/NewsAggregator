# -*- encoding:utf-8 -*-
"""
                                                  - File description -
------------------------------------------------------------------------------------------------------------------------
Base exception classes.

TODO: Este fichero podría contener todas las clases base de cada archivo exception, para que cada tipo de excepción
 pueda ser identificada por su clase base y puedan ser atrapadas en bloques except con más facilidad. Se propone cambiar
 el nombre de BaseAppException por algo como RootException y crear BusinessLogicException, ValidationException,
 ApiException, etc... a partir de ella. Preguntarse si es necesario crear estas clases "dummy" para esta clasificación,
 ¿hay una mejor manera de clasificar excepciones?.
TODO: Revisar los códigos HTTP para cada excepción, ¿son los más adecuados en cada caso?.
TODO: ¿Tiene sentido fijar los valores de error_code y recommendation_message en __init__?, quizás dejarlos a nivel
 sería mejor alternativa.
"""


class BaseAppException(Exception):

    # All exceptions will have an unique alphanumeric code and a default error message.
    exception_code = ""
    _default_error_message = "An error occurred, please try again"

    # List that contains the exception codes of all the exception classes. Used to control that every exception class
    # has an unique exception code.
    # TODO: Este miembro es visible en el resto de subclases, lo cual es incorrecto. Encontrar la forma de mantener
    #  esta lógica sin propagar esta lista.
    __exception_code_registry = []

    def __init__(self, error_message: str = None, formatting_data: dict = None,
                 recommendation_message: str = None) -> None:
        super(BaseAppException, self).__init__()
        self._error_message = error_message or self._default_error_message
        self._formatting_data = formatting_data or {}

        # A HTTP status code that will be returned along the error data as the server HTTP response. Depending on
        # the exception, this code can change, but 409 can be used as the standard for internal, business-logic
        # related errors.
        # See:
        #   - https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/409
        #   - https://softwareengineering.stackexchange.com/q/341732/402704
        self._http_status_code = 409

        # Some exceptions can give a recommendation to the caller on how to fix an error on their side.
        self._recommendation_message = None

    def __init_subclass__(cls, **kwargs) -> None:
        """Enforces the uniqueness of exception_code for every exception subclass"""
        super(BaseAppException, cls).__init_subclass__(**kwargs)
        exception_code = getattr(cls, 'exception_code')
        if not exception_code or (exception_code and exception_code in cls.__exception_code_registry):
            raise RuntimeError(f"The exception class {cls.__name__} has an already used exception code")

        cls.__exception_code_registry.append(exception_code)

    @property
    def error_message(self) -> str:
        return self._error_message.format(**self._formatting_data)

    @property
    def http_status_code(self) -> int:
        return self._http_status_code

    @property
    def recommendation_message(self) -> str:
        return self._recommendation_message

    def __str__(self) -> str:
        """
        Return a string representation of the error. The error message will be formatted with the data held in the
        instance
        """
        return f"An error occurred: {self._error_message.format(**self._formatting_data)}"

    def __repr__(self) -> str:
        """Returns a string representation of the instance that can be used to re-create it"""
        return f"{self.__class__.__name__}(\"{self.error_message}\", {self._formatting_data})"
