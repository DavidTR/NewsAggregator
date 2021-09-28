# -*- encoding:utf-8 -*-
"""
                                                  - File description -
------------------------------------------------------------------------------------------------------------------------

"""
from logic.users import UserData
from test.base import TestBase


class TestUserData(TestBase):

    def setUp(self) -> None:
        """Setup procedure for the test"""
        self._service_class = UserData

        self._valid_parameters_test_values = {
            "name": "Test"
        }

