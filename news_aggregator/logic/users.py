# -*- encoding:utf-8 -*-
"""
                                                  - File description -
------------------------------------------------------------------------------------------------------------------------

"""
from typing import Any

from sqlalchemy.sql import select

from db.connection import database_engine
from db.mapping.users import Users
from logic.base import BaseService
from util.validators import is_valid_email, surpasses_maximum_length


class UserData(BaseService):

    def __init__(self, *args, **kwargs):
        super(UserData, self).__init__(*args, **kwargs)
        self._service_parameters_constraints = {
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
            }
        }

    def preliminary_checks(self) -> Any:
        # No preliminary checks needed.
        pass

    def service_logic(self) -> dict:
        # Get the database record for the user.
        user_query = select(Users).where(Users.email == self._service_parameters["email"])
        user_record = None

        with database_engine.connect() as database_connection:
            user_record = database_connection.execute(user_query).first()

        print(user_record)


if __name__ == '__main__':

    instance = UserData()
    instance.set_parameters({"email": "test1@test.com"})
    instance.service_logic()
