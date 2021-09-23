# -*- encoding:utf-8 -*-
"""
                                                  - File description -
------------------------------------------------------------------------------------------------------------------------

"""
import abc

from exception.validation import MissingField, InvalidType, ValidationException


class BaseServiceClass(abc.ABC):
    """
    This class will have the required structure for all the service classes to share.

    Every service class will have the following components:
     - One main method, "execute", which will implement the logic of the service.
     - A special method "validate_parameters" which validates the type and format of the parameters that the
    service operates with.
    """

    @abc.abstractmethod
    def __init__(self, *args, **kwargs):
        """This method must load the parameters."""
        super(BaseServiceClass, self).__init__(*args, **kwargs)

        # The service parameters, that will be loaded in the API.
        self._service_parameters = {}

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
        """
        self._service_parameters_constraints = {}

    def set_parameters(self, **kwargs):
        """
        Class method that sets the service parameters and stores them for later use. The parameters will be used
        internally only, so no getter needs to be implemented
        """
        self._service_parameters = kwargs

    @abc.abstractmethod
    def execute(self) -> None:
        """The service logic will be implemented here by the subclasses"""
        pass

    def validate_parameters(self) -> None:
        """
        Each service class will implement this method and write their own parameter validation logic. It will
        be encapsulated in the class, fomenting the cohesion and easing the test writing.

        Look before you leap style (https://docs.python.org/3/glossary.html#term-lbyl).
        """
        if not self._service_parameters_constraints or self._service_parameters_constraints == {}:
            raise RuntimeError(f"The class {self.__class__.__name__} has not declared the required parameter "
                               f"constraints")

        self._validate_parameters_type()
        self._validate_parameters_format()

    def _validate_parameters_type(self) -> None:
        """Validates the type of the service parameters"""

        try:
            # Check if the required parameters have been provided.
            for parameter_name, parameter_constraint in self._service_parameters_constraints.items():
                if parameter_name not in self._service_parameters and not parameter_constraint["is_optional"]:
                    raise MissingField(error_message=f"The parameter {parameter_name} has not been provided")

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
        """Validates the parameters format"""
        # At this point, we are sure that the parameters are all present and they have the correct type.
        for parameter_name, parameter_value in self._service_parameters.items():
            parameter_validations = self._service_parameters_constraints[parameter_name]

            for parameter_validator in parameter_validations["validators"]:
                validator_parameters = parameter_validator["parameters"]

                # Substitute the first value for the parameter value and call the validator with the rest of the
                # parameters.
                validator_parameters[0] = parameter_value
                parameter_validator["function"](*validator_parameters)




