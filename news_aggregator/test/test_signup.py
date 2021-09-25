# -*- encoding:utf-8 -*-
"""
                                                  - File description -
------------------------------------------------------------------------------------------------------------------------

"""
import random
import string
import unittest

from exception.validation import IncorrectFormat, InsufficientLength, \
    NotEnoughSpecialCharacters, NotEnoughCapitalLetters, InvalidType, MaxLengthExceeded, MissingField
from logic.users import SignUp


class SignUpTest(unittest.TestCase):

    def _test_print(self, printable: str) -> None:
        """Special method that prints the given string only if the verbose flag is set to True"""
        if self.verbose:
            print(printable)

    def setUp(self) -> None:
        """Setup procedure for the test"""
        # If set to True, the test will print debugging strings.
        self.verbose = True
        self.service_class = SignUp

        # Set of valid values for each parameter of the service. Useful to test the parameter validation methods.
        self._valid_parameters_test_values = {
            "name": "Test",
            "surname": "Test Test",
            "email": "test@test.com",
            "password": "PaSsw?!-;ord"
        }

        # This structure contains all the data required to test the type validity and format correctness of the
        # parameters, mimicking the process that the service class follows. Each parameter will be substituted by
        # an invalid type/format example so as to ensure that the right exception is raised.
        self.service_parameters_constraints = {
            "name": {
                "type": str,
                "validations": [
                    {
                        "incorrect_parameter_value": "Te",
                        "raises": InsufficientLength
                    },
                    {
                        "incorrect_parameter_value": "Testtesttesttesttesttesttesttesttesttest",
                        "raises": MaxLengthExceeded
                    }
                ],
                "is_optional": False
            },
            "surname": {
                "type": str,
                "validations": [
                    {
                        "incorrect_parameter_value": "Te",
                        "raises": InsufficientLength
                    },
                    {
                        "incorrect_parameter_value": "Testtesttesttesttesttesttesttesttesttesttesttesttesttesttest",
                        "raises": MaxLengthExceeded
                    }
                ],
                "is_optional": False
            },
            "email": {
                "type": str,
                "validations": [
                    {
                        "incorrect_parameter_value": "Test@",
                        "raises": IncorrectFormat
                    },
                    {
                        "incorrect_parameter_value": "Testtesttesttesttest@test.com",
                        "raises": MaxLengthExceeded
                    }
                ],
                "is_optional": False
            },
            "password": {
                "type": str,
                "validations": [
                    {
                        "incorrect_parameter_value": "Pas!?_;",
                        "raises": InsufficientLength
                    },
                    {
                        "incorrect_parameter_value": "Passw!?_;",
                        "raises": NotEnoughCapitalLetters
                    },
                    {
                        "incorrect_parameter_value": "PassworD123",
                        "raises": NotEnoughSpecialCharacters
                    }
                ],
                "is_optional": False
            }
        }

    def test_invalid_parameters_type(self):
        """Tests that the validation logic raises the right exception when a parameter has an invalid type"""
        test_available_types = [None, int, float, str]
        list_ascii_letters = list(string.ascii_letters)
        service_instance = self.service_class()

        # Generates random values for every available parameter. As this method is testing invalid types only,
        # each parameter will be validated against the service class with a random value of a different type,
        # simulating data of an invalid type provided by the user.
        for parameter_name, parameter_data in self.service_parameters_constraints.items():
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

    def test_incorrect_parameters_format(self):
        """Test for parameters with an incorrect format"""
        # In this first version of the test, an incorrect static value is used for each field. They could be calculated
        # like in the invalid type test, but that could cost too much time. Compared with the benefits we could
        # earn, isn't worthy.
        service_instance = self.service_class()

        # TODO: Habría que añadir más variedad a este test.
        for parameter_name, parameter_data in self.service_parameters_constraints.items():
            for validator_data in parameter_data["validations"]:
                self._test_print(f"Testing the correctness of the argument {parameter_name} with the value "
                                 f"{validator_data['incorrect_parameter_value']}")
                test_parameters = self._valid_parameters_test_values.copy()
                test_parameters[parameter_name] = validator_data["incorrect_parameter_value"]
                service_instance.set_parameters(test_parameters)

                with self.assertRaises(validator_data["raises"]):
                    service_instance.validate_parameters()

    def test_missing_parameters(self):
        """Test to ensure that an invalid name or a missing parameter triggers the required exception"""
        service_instance = self.service_class()

        for parameter_name, parameter_data in self.service_parameters_constraints.items():

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


if __name__ == '__main__':
    unittest.main()
