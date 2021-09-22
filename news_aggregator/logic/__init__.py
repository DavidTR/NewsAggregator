# -*- encoding:utf-8 -*-
"""
                                                  - File description -
------------------------------------------------------------------------------------------------------------------------
All business logic and services files will be in this module.

"""
import abc


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

    @abc.abstractmethod
    def execute(self) -> None:
        """The service logic will be implemented here by the subclasses"""
        pass

    @abc.abstractmethod
    def validate_parameters(self) -> None:
        """
        Each service class will implement this method and write their own parameter validation logic. It will
        be encapsulated in the class, fomenting the cohesion and easing the test writing
        """
        pass
