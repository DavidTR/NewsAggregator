# -*- encoding:utf-8 -*-
"""
                                                  - File description -
------------------------------------------------------------------------------------------------------------------------
Base class for all the services.

TODO: Crear tutorial sobre cómo heredar de esta clase y cómo fijar los valores. Documentar en README.

"""
import abc
import copy
from typing import Type, Union

from sqlalchemy import select

from db.connection import database_engine
from db.mapping.users import Sessions
from exception.sessions import SessionDoesNotExist, SessionIsNotAlive
from exception.validation import MissingField, InvalidType
from util.logging import AppLogger


class BaseService(abc.ABC):
    """
    This class will have the required structure for all the service classes to inherit from. This will be the default
    service API for each application service.

    Every service class will have the following components:
        TODO

    The correct flow of execution must be ensured by the programmer and it should look like so:
        - service_instance = ServiceClass(*args, **kwargs)
        - service_instance.set_parameters(parameters_dict)
        - service_instance.validate_parameters()
        - service_instance.execute()
    If the methods are not called in this order, the service won't work accordingly, raising KeyErrors at best and
    generating database inconsistencies at worst.
    """

    @abc.abstractmethod
    def __init__(self, *args, **kwargs):
        """This method must load the parameters."""
        super(BaseService, self).__init__(*args, **kwargs)

        # The service parameters, that will be loaded in the API.
        self._parameters = None

        # This structure will help the validate_parameters when the parameters are validated. The idea is that
        # every service will declare their own parameter names, types and validators, so the method can perform the
        # validations over each of them automatically.

        # Each element of this dictionary must follow the following structure. An exception will be raised otherwise:
        """
        # String that identifies the name (preferably the sames as the related API argument) of the parameter.
        PARAMETER_NAME: {
            # Type of the parameter. Only basic types like str, int, float are supported.
            "type": PARAMETER_TYPE,
            "validators": [
                {
                    # Feel free to add all the validators you need. "PARAMETER_VALUE" is a placeholder that will be
                    # replaced with the parameter value when the validator function is called. "PARAMETER_VALUE" must
                    # be always the first value in the list.
                    "function": VALIDATOR_FUNCTION (see util/validators.py),
                    "parameters": ["PARAMETER_VALUE", *validator_args],
                }
            ],
            # If the parameter is optional, set this field to True. 
            "is_optional": PARAMETER_OPTIONALITY
        },
        
        NOTE: If the service does not require any parameters, this structure must be an empty dictionary ({}).
        """
        # TODO: ¿Mover esta parte al API y que se hagan allí las validaciones?. Sería más lógico, pero no se podrían
        #  testear en tests unitarios.
        self._parameters_constraints = None

        # Easier access to the logger for internal use of all service classes.
        self._logger = AppLogger().logger

        # Internal data to be shared across internal methods.
        self._internal_data = None

        # Flag that configures this class to check a session and user ID's validity, as it's required by the
        # implementing class. Set to False by default.
        # The requires_login class decorator sets this flag to True among other things, see it for more information.
        self._check_session = False

    def set_parameters(self, service_parameters: dict) -> None:
        """
        Class method that sets the service parameters and stores them for later use. Extra parameters will be ignored.
        """
        # deepcopy creates a new object, so parameters will be pointing to a newly created object in memory.
        self._parameters = copy.deepcopy(service_parameters)

        # Delete the parameters that the service is not aware of.
        for parameter_name, parameter_value in service_parameters.items():
            if parameter_name not in self._parameters_constraints.keys():
                del self._parameters[parameter_name]

    def check_session(self) -> None:
        """Checks if the given session ID matches an alive session"""

        # TODO: No me gusta del todo dejar esta comprobación aquí y que todos los servicios la tengan, pero la
        #  alternativa que se me ocurre es dejarla en la clase base del procesador, lo cual tampoco me parece
        #  correcto. El dejar esto aquí aumentaría la cohesión sin incurrir en un aumento del acoplamiento con la
        #  clase de procesador.
        # TODO: Todos los servicios logados deberían incorporar session_id y user_id como parámetros. ¿decorator?.

        if self._check_session:
            session_query = select(Sessions.is_alive).where(Sessions.session_id == self._parameters["session_id"])

            with database_engine.connect() as database_connection:
                session = database_connection.execute(session_query).first()

            if not session:
                raise SessionDoesNotExist()

            if not session.is_alive:
                raise SessionIsNotAlive()

    def service_logic(self) -> dict:
        """
        Default execution flow for every service. There are several hooks for the children classes to implement. If
        needed, this method can be overridden for a more customizable structure.
        """
        self._parameters_preliminary_checks()
        self._load_data()
        self._preliminary_checks()
        self._execute()
        self._post_execute()

        return self._build_response()

    def _parameters_preliminary_checks(self) -> None:
        """Perform early checks in parameters. This will allow the service to abort execution if needed"""
        pass

    def _load_data(self) -> None:
        """
        Loads data required by the service logic. This method will be responsible of not leaving opened resources.
        """
        pass

    def _preliminary_checks(self) -> None:
        """
        Performs preliminary checks, usually over the data loaded in the method _load_data. This method is responsible
        of ensuring that the data is safe to be used in the following methods. For example, assuring that a data
        retrieved from an external URL has the required content, or an email is not already registered (for a signup
        or user data edit request).
        """
        pass

    def _execute(self) -> None:
        """
        Perform the main actions of the service.
        """
        pass

    def _post_execute(self) -> None:
        """
        After executing the main instructions, extra actions can be performed here, like sending notifications, for
        example.
        """
        pass

    def _build_response(self) -> Union[dict, list]:
        """Composes the response in a well-formed dictionary using the required data"""
        # TODO: Estudiar formato adecuado para estandarizar la respuesta.
        return {}

    @staticmethod
    def _get_ok_response() -> dict:
        """Returns a well-formed empty response"""
        return {"data": {}, "error": {}}

    def validate_parameters(self) -> None:
        """
        Each service class will implement this method and write their own parameter validation logic. It will
        be encapsulated in the class, fomenting the cohesion and easing the test writing.

        Look before you leap style (https://docs.python.org/3/glossary.html#term-lbyl).
        """
        # The service parameters constraints dictionary must be filled (even if its with an empty dict).
        if not self._parameters_constraints:
            raise RuntimeError(f"The service class {self.__class__.__name__} has not declared the required parameter "
                               f"constraints")

        # If there are service parameters constraints and the parameters are not set, an error is raised, as the
        # programmer forgot about calling the set_parameters method.
        if not self._parameters_constraints == {} and self._parameters is None:
            raise RuntimeError(f"The service class {self.__class__.__name__} has not set its parameters")

        self._check_parameters_provided()
        self._parse_parameters()
        self._validate_parameters_format()

    def _check_parameters_provided(self) -> None:
        """Checks if the required parameters have been provided"""
        for parameter_name, parameter_constraint in self._parameters_constraints.items():
            if parameter_name not in self._parameters.keys() and not parameter_constraint["is_optional"]:
                raise MissingField(error_message=f"The parameter {parameter_name} has not been provided")

    def _parse_parameters(self) -> None:
        """Parses the parameters by checking their type and then casting them to the required data type"""

        # Check if the required parameters have been provided.
        for parameter_name, parameter_constraint in self._parameters_constraints.items():

            # The type won't be checked in an optional parameter that hasn't been provided.
            if parameter_constraint["is_optional"] and parameter_name not in self._parameters:
                continue

            # TODO: Imprimir este mensaje para que el usuario de la API vea los tipos adecuadamente
            #  (por ejemplo: <str> -> String). Según documentación a generar en Swagger.
            # Parse the parameter and update it.
            try:
                self._parameters[parameter_name] = parameter_constraint["type"](self._parameters[parameter_name])
            except (TypeError, ValueError):
                raise InvalidType(error_message=f"The field {parameter_name} has an invalid type: "
                                                f"{type(self._parameters[parameter_name])}. "
                                                f"Expected type: {parameter_constraint['type']}")

    def _validate_parameters_format(self) -> None:
        """Validates the format of the service parameters"""
        # At this point, we are sure that the parameters are all present and they have the correct type.
        for parameter_name, parameter_value in self._parameters.items():
            parameter_validations = self._parameters_constraints[parameter_name]

            for parameter_validator in parameter_validations["validators"]:
                validator_parameters = parameter_validator["parameters"]

                # Substitute the first value for the parameter value and call the validator with the rest of the
                # parameters.
                validator_parameters[0] = parameter_value
                parameter_validator["function"](*validator_parameters)


ServiceClassType = Type[BaseService]
