# -*- encoding:utf-8 -*-
"""
                                                  - File description -
------------------------------------------------------------------------------------------------------------------------

"""
from sqlalchemy.sql import select

from db.connection import database_engine
from db.mapping.users import Users
from exception.users import EmailAlreadyRegistered
from logic.base import BaseServiceClass
from util.validators import has_minimum_length, is_valid_email, has_minimum_capital_letters, \
    contains_special_characters, surpasses_maximum_length


class SignUp(BaseServiceClass):

    def __init__(self):
        super(SignUp, self).__init__()
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
        """Checks if the user identified by "email" already exists in the database"""
        user_email = self._service_parameters["email"]

        is_user_signed_up_query = select(Users).where(Users.email == user_email)

        with database_engine.connect() as database_connection:
            is_user_signed_up = database_connection.execute(is_user_signed_up_query).first()
            if is_user_signed_up:
                raise EmailAlreadyRegistered()

    def service_logic(self) -> None:
        """Implements the service logic"""


class UserData:

    @staticmethod
    def retrieve_user_data(user: Users) -> dict:
        """Reads and returns the data of a given user"""
        """
        session = Session()
        user_data = {}

        try:
            user_data = session.query(Users).filter_by(id=user.id).all()
            if not user_data:
                raise UserNotFound()
        except:
            # TODO
            pass
        finally:
            session.close()

        return user_data
        """
