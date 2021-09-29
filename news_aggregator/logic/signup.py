# -*- encoding:utf-8 -*-
"""
                                                  - File description -
------------------------------------------------------------------------------------------------------------------------
Signup service class.

"""

from typing import Any

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
        self._service_parameters_constraints = {
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

    def preliminary_checks(self) -> None:

        # Checks if the user identified by "email" already exists in the database
        user_email = self._service_parameters["email"]

        is_email_already_used_query = select(Users).where(Users.email == user_email)

        with database_engine.connect() as database_connection:
            is_email_already_used = database_connection.execute(is_email_already_used_query).first()
            if is_email_already_used:
                raise EmailAlreadyInUse()

    def service_logic(self) -> dict:

        # This class does not have extra logic (YET)
        # TODO: Enviar correos electrónicos o notificaciones.
        pass

    def _save_to_database(self) -> None:

        password = self._service_parameters["password"]
        hashed_password = hash_password(password)

        new_user_query = insert(Users).values(name=self._service_parameters["name"],
                                              surname=self._service_parameters["surname"],
                                              email=self._service_parameters["email"],
                                              password=hashed_password)

        # TODO: Capturar esta excepción y mostrar un mensaje genérico, apuntarla en algún lado.
        # The methods "commit" and "rollback" are invoked automatically if context managers are used with engines or
        # sessions. SQLAlchemy recommends this as a best practice:
        # https://docs.sqlalchemy.org/en/13/core/connections.html?highlight=dispose#using-transactions
        with database_engine.connect() as database_connection:
            database_connection.execute(new_user_query)
