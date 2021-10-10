# -*- encoding:utf-8 -*-
"""
                                                  - File description -
------------------------------------------------------------------------------------------------------------------------

"""
from sqlalchemy import update
from sqlalchemy.sql import select

from db.connection import database_engine
from db.mapping.users import Users
from exception.users import UserNotFound, NoNewUserDataProvided
from logic.base import BaseService
from util.validators import is_integer_too_small, is_integer_too_large, has_minimum_length, surpasses_maximum_length, \
    is_valid_email


class UserDataModification(BaseService):

    def __init__(self, *args, **kwargs):
        super(UserDataModification, self).__init__(*args, **kwargs)
        self._parameters_constraints = {
            "user_id": {
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
            },
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
                "is_optional": True
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
                "is_optional": True
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
                "is_optional": True
            },
        }

    def _parameters_preliminary_checks(self):

        # If no update parameters were provided (name, surname or email), abort the execution.
        # As user_id is not optional, if only one parameter is provided, the exception is raised.
        if len(self._parameters.keys()) == 1:
            raise NoNewUserDataProvided()

    def _load_data(self) -> None:

        user_record_query = select(Users).where(Users.id == self._parameters["user_id"])

        with database_engine.connect() as database_connection:
            user_record = database_connection.execute(user_record_query).first()

        self._internal_data = {"user_record": user_record}

    def _preliminary_checks(self) -> None:

        if not self._internal_data["user_record"]:
            raise UserNotFound()

    def _execute(self) -> None:

        # Update user data.
        user_data_update_query = update(Users).where(Users.id == self._parameters["user_id"])

        new_user_name, new_user_surname, new_user_email = self._parameters.get('name'), self._parameters.get('surname'), self._parameters.get('email')

        if new_user_name:
            user_data_update_query = user_data_update_query.values(name=new_user_name)

        if new_user_surname:
            user_data_update_query = user_data_update_query.values(surname=new_user_surname)

        if new_user_email:
            user_data_update_query = user_data_update_query.values(email=new_user_email)

        with database_engine.connect() as database_connection:
            database_connection.execute(user_data_update_query)


if __name__ == '__main__':
    instance = UserDataModification()
    instance.set_parameters({"user_id": 1, "name": "UPDATED", "surname": "UPDATED", "email": "updated@test.com"})
    instance.validate_parameters()
    print(instance.service_logic())
