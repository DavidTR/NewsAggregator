# -*- encoding:utf-8 -*-
"""
                                                  - File description -
------------------------------------------------------------------------------------------------------------------------

"""
import random
import string

from const.data import MIN_INT_VALUE, MAX_INT_VALUE
from exception.validation import InvalidType, MissingField, IntegerTooLarge, IntegerTooSmall
from logic.users import UserData
from test.base import TestBase


class TestUserData(TestBase):

    def setUp(self) -> None:
        """Setup procedure for the test"""
        self._service_class = UserData

        self._valid_parameters_test_values = {
            "user_id": 1
        }

        self._service_parameters_constraints = {
            "user_id": {
                "type": int,
                "validations": [
                    {
                        "incorrect_parameter_value": MAX_INT_VALUE,
                        "raises": IntegerTooLarge
                    },
                    {
                        "incorrect_parameter_value": MIN_INT_VALUE,
                        "raises": IntegerTooSmall
                    }
                ],
                "is_optional": False
            }
        }

    def test_invalid_parameters_type(self) -> None:
        """Tests that the validation logic raises the right exception when a parameter has an invalid type"""
        test_available_types = [None, int, float, str]
        list_ascii_letters = list(string.ascii_letters)
        service_instance = self._service_class()

        # Generates random values for every available parameter. As this method is testing invalid types only,
        # each parameter will be validated against the service class with a random value of a different type,
        # simulating data of an invalid type provided by the user.
        for parameter_name, parameter_data in self._service_parameters_constraints.items():
            for test_type in test_available_types:
                if parameter_data["type"] != test_type:
                    if test_type == int:
                        test_value = random.Random().randint(1, 999999)
                    elif test_type == float:
                        test_value = round(random.uniform(1, 999999), 4)
                    elif test_type == str:
                        random.shuffle(list_ascii_letters)
                        test_value = ''.join(list_ascii_letters)
                    else:
                        # Mainly for None, but any extra default cases will end up here if it has not a special way
                        # of generating a random value.
                        test_value = test_type

                    self._test_print(f"Testing invalid type for parameter {parameter_name}, which type is "
                                     f"{parameter_data['type']}. Computed test value: {test_value}, "
                                     f"of type {test_type}")

                    # In order to only test one parameter at a time, a copy of the default dictionary (which contains
                    # valid values for all the service parameter) is used. The value of the parameter that is being
                    # tested is then substituted by the one calculated previously.
                    test_parameters = self._valid_parameters_test_values.copy()
                    test_parameters[parameter_name] = test_value

                    self._test_print(f"Test parameters dictionary ready to be assigned to the service instance: "
                                     f"{test_parameters}")
                    service_instance.set_parameters(test_parameters)

                    # Check if the method raises the expected exception.
                    # TODO: Si la excepción se acopla un poco más al campo que está comprobando, debería reflejarse
                    #  aquí (por ejemplo: Nombre del campo que la provoca).
                    with self.assertRaises(InvalidType):
                        service_instance.validate_parameters()

    def test_incorrect_parameters_format(self) -> None:
        """Test for parameters with an incorrect format"""
        # In this first version of the test, an incorrect static value is used for each field. They could be calculated
        # like in the invalid type test, but that could cost too much time. Compared with the benefits we could
        # earn, isn't worthy.
        service_instance = self._service_class()

        # TODO: Habría que añadir más variedad a este test.
        for parameter_name, parameter_data in self._service_parameters_constraints.items():
            for validator_data in parameter_data["validations"]:
                self._test_print(f"Testing the correctness of the argument {parameter_name} with the value "
                                 f"{validator_data['incorrect_parameter_value']}")
                test_parameters = self._valid_parameters_test_values.copy()
                test_parameters[parameter_name] = validator_data["incorrect_parameter_value"]
                service_instance.set_parameters(test_parameters)

                with self.assertRaises(validator_data["raises"]):
                    service_instance.validate_parameters()

    def test_missing_parameters(self) -> None:
        """Test to ensure that an invalid name or a missing parameter triggers the required exception"""
        service_instance = self._service_class()

        for parameter_name, parameter_data in self._service_parameters_constraints.items():

            # If the parameter is optional, no exception will be raised if it's not set.
            if parameter_data["is_optional"]:
                continue

            missing_test_parameters = self._valid_parameters_test_values.copy()
            del missing_test_parameters[parameter_name]

            self._test_print(f"Checking if the service raises an error when the parameter {parameter_name} is not "
                             f"given")

            service_instance.set_parameters(missing_test_parameters)
            with self.assertRaises(MissingField):
                service_instance.validate_parameters()

    def test_service_logic(self) -> None:
        """Tests the service logic"""
        # TODO: Me gustaría comprobar que la respuesta tenga la estructura adecuada, pero para ello se necesitaría
        #  mockear los registros de base de datos que acepta el método service_logic. ¿Debería hacerse así o
        #  directamente no se testea nada?
        pass
