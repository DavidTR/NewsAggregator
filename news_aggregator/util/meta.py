# -*- encoding:utf-8 -*-
"""
                                                  - File description -
------------------------------------------------------------------------------------------------------------------------
File for metaprogramming assets (decorators, metaclasses and such).
"""
from util.validators import has_minimum_length, is_integer_too_large, is_integer_too_small


def requires_login(cls):
    """
    Decorator that can be applied to service classes for which an alive session is required to be executed.
    This decorator will modify the class' __init__ method, automatically adding an user_id and a session_id
    parameters and setting the _check_session flag to True, avoiding unnecessary boilerplate code.

    Every class that requires a session must ask for an user ID and a session ID. Both this parameters will be
    incorporated in the _parameters_constraints structure, so the base class' method check_session_if_required
    can test the validity of the session provided.
    """
    original_init = cls.__init__

    def new_init(self, *args, **kwargs):

        # Call the original __init__ method, which populates _parameters_constraints, among other stuff.
        original_init(self, *args, **kwargs)

        # Set this flag to True so cls checks the provided session.
        self._check_session = True

        # Add user_id and password (if not present) as required parameters in _parameters_constraints structure.
        if "user_id" not in self._parameters_constraints.keys():
            self._parameters_constraints["user_id"] = {
                "type": int,
                "validators": [
                    {
                        "function": is_integer_too_large,
                        "parameters": ["PARAMETER_VALUE"]
                    },
                    {
                        "function": is_integer_too_small,
                        "parameters": ["PARAMETER_VALUE"]
                    }],
                "is_optional": False
            }

        if "session_id" not in self._parameters_constraints.keys():
            self._parameters_constraints["session_id"] = {
                "type": str,
                "validators": [
                    {
                        "function": has_minimum_length,
                        "parameters": ["PARAMETER_VALUE", 60]
                    }
                ],
                "is_optional": False
            }
    # A decorator changes the object on which is applied (function, class, etc...).
    cls.__init__ = new_init

    return cls
