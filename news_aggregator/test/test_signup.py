# -*- encoding:utf-8 -*-
"""
                                                  - File description -
------------------------------------------------------------------------------------------------------------------------

"""
from unittest import TestCase

from exception.parameters import InvalidParameterType
from logic.users import SignUp


class SignUpTest(TestCase):

    def setUp(self) -> None:
        self.service_class = SignUp

    def arguments_validation(self):
        """Tests if the parameter validation works correctly"""
        parameter_tests = {

        }

        self.assertRaises(InvalidParameterType)

    def _name_parameter_invalid_type(self):
        """Test to ensure that an invalid name triggers the correct exception"""
