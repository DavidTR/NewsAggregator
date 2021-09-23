# -*- encoding:utf-8 -*-
"""
                                                  - File description -
------------------------------------------------------------------------------------------------------------------------

"""
import random
import string
import unittest

from exception.validation import IncorrectFormat, InsufficientLength, \
    NotEnoughSpecialCharacters, NotEnoughCapitalLetters, InvalidType
from logic.users import SignUp
from util.validators import email_format_validator, has_minimum_length, has_minimum_capital_letters, \
    contains_special_characters


class SignUpTest(unittest.TestCase):

    def _test_print(self, printable: str) -> None:
        """Special method that prints the given string only if the verbose flag is set to True"""
        if self.verbose:
            print(printable)

    def setUp(self) -> None:
        """Setup procedure for the test"""
        # If set to True, the test will print
        self.verbose = True
        self.service_class = SignUp
        self.service_parameters = {
            "name": {
                "type": str,
                "validators": [
                    {
                        "function": has_minimum_length,
                        "parameters": ["PARAMETER_VALUE", 25],
                        "raises": IncorrectFormat
                    }
                ],
                "valid_example": "Test"
            },
            "surname": {
                "type": str,
                "validators": [
                    {
                        "function": has_minimum_length,
                        "parameters": ["PARAMETER_VALUE", 40],
                        "raises": InsufficientLength
                    }
                ],
                "valid_example": "Test Test"
            },
            "email": {
                "type": str,
                "validators": [
                    {
                        "function": email_format_validator,
                        "parameters": ["PARAMETER_VALUE"],
                        "raises": IncorrectFormat
                    }
                ],
                "valid_example": "test@test.com"
            },
            "password": {
                "type": str,
                "validators": [
                    {
                        "function": has_minimum_length,
                        "parameters": ["PARAMETER_VALUE", 8],
                        "raises": InsufficientLength
                    },
                    {
                        "function": has_minimum_capital_letters,
                        "parameters": ["PARAMETER_VALUE"],
                        "raises": NotEnoughCapitalLetters
                    },
                    {
                        "function": contains_special_characters,
                        "parameters": ["PARAMETER_VALUE"],
                        "raises": NotEnoughSpecialCharacters
                    },
                ],
                "valid_example": "PaSsw?!-;ord"
            }
        }

    def test_invalid_type_parameters(self):
        """Tests that the validation logic raises the right exception when a parameter has an invalid type"""
        test_available_types = [None, int, float, str]
        list_ascii_letters = list(string.ascii_letters)
        service_instance = self.service_class()

        default_parameter_dict = {parameter_name: parameter_data["valid_example"] for parameter_name, parameter_data in self.service_parameters.items()}

        # Generates random values for every available parameter. As this method is testing invalid types only,
        # each parameter will be validated against the service class with a random value of a different type,
        # simulating data of an invalid type provided by the user.
        for parameter_name, parameter_data in self.service_parameters.items():
            for test_type in test_available_types:
                if parameter_data["type"] != test_type:
                    if test_type == int:
                        test_value = random.Random().randint(1, 999)
                    elif test_type == float:
                        test_value = round(random.uniform(1, 999), 4)
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
                    test_parameters = default_parameter_dict.copy()
                    test_parameters[parameter_name] = test_value

                    self._test_print(f"Test parameters dictionary ready to be assigned to the service instance: "
                                     f"{test_parameters}")
                    service_instance.set_parameters(**test_parameters)

                    # Check if the method raises the expected exception.
                    with self.assertRaises(InvalidType):
                        service_instance.validate_parameters()

    def _test_incorrect_format_parameters(self):
        """Test for parameters with an incorrect format"""
        pass

    def _name_parameter_invalid_type(self):
        """Test to ensure that an invalid name triggers the correct exception"""
        pass


if __name__ == '__main__':
    unittest.main()
