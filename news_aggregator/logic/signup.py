# -*- encoding:utf-8 -*-
"""
                                                  - File description -
------------------------------------------------------------------------------------------------------------------------
Signup service class.

"""

from sqlalchemy import select, insert

from db.connection import database_engine
from db.mapping.users import Users
from exception.users import EmailAlreadyInUse
from logic.base import BaseService
from util.security import hash_password
from util.validators import has_minimum_length, is_valid_email, has_minimum_capital_letters, \
    contains_special_characters, surpasses_maximum_length


class SignUp(BaseService):

    def __init__(self, *args, **kwargs):
        super(SignUp, self).__init__(*args, **kwargs)
        self._parameters_constraints = {
            "name": {
                "type": str,
                "validators": [
                    {
                        "function": has_minimum_length,
                        "parameters": ["PARAMETER_VALUE", 3]
                    },
                    {
                        "function": surpasses_maximum_length,
                        "parameters": ["PARAMETER_VALUE", 25]
                    }
                ],
                "is_optional": False
            },
            "surname": {
                "type": str,
                "validators": [
                    {
                        "function": has_minimum_length,
                        "parameters": ["PARAMETER_VALUE", 3]
                    },
                    {
                        "function": surpasses_maximum_length,
                        "parameters": ["PARAMETER_VALUE", 50]
                    }
                ],
                "is_optional": False
            },
            "email": {
                "type": str,
                "validators": [
                    {
                        "function": is_valid_email,
                        "parameters": ["PARAMETER_VALUE"]
                    },
                    {
                        "function": surpasses_maximum_length,
                        "parameters": ["PARAMETER_VALUE", 25]
                    }
                ],
                "is_optional": False
            },
            "password": {
                "type": str,
                "validators": [
                    {
                        "function": has_minimum_length,
                        "parameters": ["PARAMETER_VALUE", 8]
                    },
                    {
                        "function": has_minimum_capital_letters,
                        "parameters": ["PARAMETER_VALUE", 2]
                    },
                    {
                        "function": contains_special_characters,
                        "parameters": ["PARAMETER_VALUE"]
                    },
                ],
                "is_optional": False
            }
        }

    def _load_data(self) -> None:

        user_record_query = select(Users).where(Users.email == self._parameters["email"])

        with database_engine.connect() as database_connection:
            user_record = database_connection.execute(user_record_query).first()

        self._internal_data["user_record"] = user_record

    def _preliminary_checks(self) -> None:

        # Check if the email is already registered in the database.
        if self._internal_data["user_record"]:
            raise EmailAlreadyInUse()

    def _execute(self) -> None:

        password = self._parameters["password"]
        hashed_password = hash_password(password)

        new_user_query = insert(Users).values(name=self._parameters["name"],
                                              surname=self._parameters["surname"],
                                              email=self._parameters["email"],
                                              password=hashed_password)

        # The methods "commit" and "rollback" are invoked automatically if context managers are used with engines or
        # sessions.
        # SQLAlchemy recommends context managers as a best practice:
        # https://docs.sqlalchemy.org/en/13/core/connections.html?highlight=dispose#using-transactions
        with database_engine.connect() as database_connection:
            database_connection.execute(new_user_query)
