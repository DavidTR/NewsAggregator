# -*- encoding:utf-8 -*-
"""
                                                  - File description -
------------------------------------------------------------------------------------------------------------------------

"""
import datetime
from typing import Union

from sqlalchemy import select, insert

from db.connection import database_engine
from db.mapping.users import Users, Sessions
from exception.sessions import AliveSessionAlreadyExists
from exception.users import UserNotFound, IncorrectPassword
from logic.base import BaseService
from util.security import create_session_id, check_password
from util.validators import has_minimum_length, is_valid_email, has_minimum_capital_letters, \
    contains_special_characters, surpasses_maximum_length


class LogIn(BaseService):

    def __init__(self, *args, **kwargs):
        super(LogIn, self).__init__(*args, **kwargs)
        self._parameters_constraints = {
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

        # TODO: Ahora este método tiene más de una responsabilidad. ¿Refactorizar para que sólo se tomaran las sesiones
        #  si existe el usuario y hacer esta comprobación en _preliminary_checks?
        if not user_record:
            raise UserNotFound()

        user_sessions_query = select(Sessions). \
            where(Sessions.user_id == user_record.id). \
            where(Sessions.is_alive == True)

        with database_engine.connect() as database_connection:
            user_sessions = database_connection.execute(user_sessions_query).all()

        self._internal_data = {"user_record": user_record, "user_sessions": user_sessions}

    def _preliminary_checks(self) -> None:

        # Check if the provided password matches with the user's.
        if not check_password(self._parameters["password"], self._internal_data["user_record"].password):
            raise IncorrectPassword()

        # If there's an already open session, abort the login process.
        if self._internal_data["user_sessions"]:
            raise AliveSessionAlreadyExists()

    def _execute(self) -> None:

        user_id = self._internal_data["user_record"].id

        session_expiration_date = datetime.datetime.now() + datetime.timedelta(minutes=5)
        session_id = create_session_id(user_id)

        new_session_query = insert(Sessions).values(user_id=user_id, session_id=session_id,
                                                    expiration_date=session_expiration_date)

        with database_engine.connect() as database_connection:
            database_connection.execute(new_session_query)

        self._internal_data["session_data"] = {"user_id": user_id, "session_id": session_id,
                                               "session_expiration_date": session_expiration_date.strftime(
                                                   "%d-%m-%Y %H:%M:%S")}

    def _build_response(self) -> Union[dict, list]:
        return self._internal_data["session_data"]


if __name__ == '__main__':
    instance = LogIn()
    instance.set_parameters({"email": "updated@test.com", "password": "PaSsw?!-;ord"})
    instance.validate_parameters()
    print(instance.service_logic())
