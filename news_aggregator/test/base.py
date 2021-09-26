# -*- encoding:utf-8 -*-
"""
                                                  - File description -
------------------------------------------------------------------------------------------------------------------------
Parent class for all classes.

This class won't have any test methods, so the unittest module doesn't try to instantiate it and run the tests, leading
to counting TestBase as a test class, when it's not. Do not add test methods to this class (even if they are abstract),
unittest will try to instantiate this class and execute its tests and it will fail because it's an abstract class.
"""
import unittest
import abc


class TestBase(unittest.TestCase, metaclass=abc.ABCMeta):

    def __init__(self, *args, **kwargs):
        super(TestBase, self).__init__(*args, **kwargs)

        # If set to True, the test will print debugging strings.
        self._verbose = None

        # Service class that being tested.
        self._service_class = None

        # Set of valid values for each parameter of the service. Useful to test the parameter validation methods.
        self._valid_parameters_test_values = None

        # This structure contains all the data required to test the type validity and format correctness of the
        # parameters. Each parameter will be substituted by an invalid type/format example so as to ensure that
        # the right exception is raised.
        self._service_parameters_constraints = None

    @abc.abstractmethod
    def setUp(self) -> None:
        """
        Setup procedure for the test. All the special variables declared in the __init__ method should be set
        here
        """
        pass

    def _test_print(self, string: str) -> None:
        """Special method that prints the given string only if the verbose flag is set to True"""
        if self._verbose:
            print(string)
