# -*- encoding:utf-8 -*-
"""
                                                  - File description -
------------------------------------------------------------------------------------------------------------------------
Base class for all the services.

TODO: Crear tutorial sobre cómo heredar de esta clase y cómo fijar los valores.
"""
import abc
import copy
from typing import Any, TypeVar, Type

from exception.base import BaseAppException
from exception.validation import MissingField, InvalidType


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
        self._service_parameters = None

        # This structure will help the validate_parameters when the parameters are validated. The idea is that
        # every service will declare their own parameter names, types and validators, so the method can perform the
        # validations over each of them automatically.

        # Each element of this dictionary must follow the following structure. An exception will be raised otherwise:
        """
        # String that identifies the name (preferably the sames as the related API argument) of the parameter.
        PARAMETER_NAME: {
            # Type of the parameter. Basic types like str, int, float are supported.
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
        self._service_parameters_constraints = None

    def set_parameters(self, service_parameters: dict) -> None:
        """
        Class method that sets the service parameters and stores them for later use. The parameters will be used
        internally only, so no getter needs to be implemented
        """
        # deepcopy creates a new object, so _service_parameters will be pointing to a newly created object in memory.
        self._service_parameters = copy.deepcopy(service_parameters)

    @abc.abstractmethod
    def preliminary_checks(self) -> Any:
        """Performs preliminary checks, so it is safe to execute the rest of the service logic and database access"""
        pass

    @abc.abstractmethod
    def service_logic(self) -> dict:
        """
        This method will contain the required business logic for the service. Like so, logic and database access
        will be separated, as needed for unit tests.
        :return Must return a dictionary with the data to be returned to the caller.
        """
        pass

    def execute(self) -> dict:
        """
        Default execution flow for every service. There are several hooks for the children classes to implement. If
        needed, this method can be overridden for a more customizable structure, depending on the service's nature
        """
        # Hook for children classes.
        self.preliminary_checks()

        # This method will implement the main service logic, which must not rely on the database.
        service_result = self.service_logic()

        # Hook for children classes.
        self._save_to_database()

        return service_result

    def validate_parameters(self) -> None:
        """
        Each service class will implement this method and write their own parameter validation logic. It will
        be encapsulated in the class, fomenting the cohesion and easing the test writing.

        Look before you leap style (https://docs.python.org/3/glossary.html#term-lbyl).
        """
        # The service parameters constraints dictionary must be filled (even if its with an empty dict).
        if not self._service_parameters_constraints:
            raise RuntimeError(f"The service class {self.__class__.__name__} has not declared the required parameter "
                               f"constraints")

        # If there are service parameters constraints and the parameters are not set, an error is raised, as the
        # programmer forgot about calling the set_parameters method.
        if not self._service_parameters_constraints == {} and self._service_parameters is None:
            raise RuntimeError(f"The service class {self.__class__.__name__} has not set its parameters")

        self._check_parameters_provided()
        self._validate_parameters_type()
        self._validate_parameters_format()

    def _check_parameters_provided(self) -> None:
        """Checks if the required parameters have been provided"""
        for parameter_name, parameter_constraint in self._service_parameters_constraints.items():
            if parameter_name not in self._service_parameters.keys() and not parameter_constraint["is_optional"]:
                raise MissingField(error_message=f"The parameter {parameter_name} has not been provided")

    def _validate_parameters_type(self) -> None:
        """Validates the type of the service parameters"""

        try:
            # Check if the required parameters have been provided.
            for parameter_name, parameter_constraint in self._service_parameters_constraints.items():
                parameter_value = self._service_parameters[parameter_name]

                # TODO: Imprimir este mensaje para que el usuario de la API vea los tipos adecuadamente
                #  (por ejemplo: <str> -> String). Según documentación a generar en Swagger.
                if type(parameter_value) != parameter_constraint["type"]:
                    raise InvalidType(error_message=f"The field {parameter_name} has an invalid type: "
                                                    f"{type(parameter_value)}. "
                                                    f"Expected type: {parameter_constraint['type']}")
        except KeyError:
            raise RuntimeError(f"The class {self.__class__.__name__} has declared an invalid parameter constraint "
                               f"structure")

    def _validate_parameters_format(self) -> None:
        """Validates the format of the service parameters"""
        # At this point, we are sure that the parameters are all present and they have the correct type.
        for parameter_name, parameter_value in self._service_parameters.items():
            parameter_validations = self._service_parameters_constraints[parameter_name]

            for parameter_validator in parameter_validations["validators"]:
                validator_parameters = parameter_validator["parameters"]

                # Substitute the first value for the parameter value and call the validator with the rest of the
                # parameters.
                validator_parameters[0] = parameter_value
                parameter_validator["function"](*validator_parameters)

    def _save_to_database(self, *args) -> Any:
        """
        Saves whichever changes the service requires to the database. If needed, this method must be invoked in
        "execute"
        """
        pass


ServiceClassType = Type[BaseService]
