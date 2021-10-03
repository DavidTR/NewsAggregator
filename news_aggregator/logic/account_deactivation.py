# -*- encoding:utf-8 -*-
"""
                                                  - File description -
------------------------------------------------------------------------------------------------------------------------
TODO: ¿Crear un nuevo archivo users.py y ubicar esta y otras clases de servicios relativos a usuarios ahí?.
"""
from typing import Any

from sqlalchemy import select, update

from db.connection import database_engine
from db.mapping.users import Users
from exception.users import UserAccountDeactivated
from logic.base import BaseService
from util.validators import is_integer_too_small, is_integer_too_large


class AccountDeactivation(BaseService):

    def __init__(self, *args, **kwargs):
        super(AccountDeactivation, self).__init__(*args, **kwargs)
        self._service_parameters_constraints = {
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
            }
        }

    def prepare(self) -> None:
        pass

    def preliminary_checks(self) -> Any:
        with database_engine.connect() as database_connection:
            user_record_query = select(Users.is_active).where(Users.id == self._service_parameters["user_id"])
            user_record = database_connection.execute(user_record_query).first()

            # TODO: ¿Haría falta una comprobación por si los datos de usuario no se encontraran o esto ya lo cubre el
            #  login?. Creo que es así, login ya cubriría:
            #   - Existencia de registro de usuario.
            #   - Estado activo de la cuenta -> Un usuario desactivado podría seguir haciendo uso de su token por un
            #   tiempo limitado tras desactivar su cuenta. O bien hacemos esta comprobación o invalidamos su token.
        if not user_record.is_active:
            raise UserAccountDeactivated()

    def service_logic(self) -> None:
        with database_engine.connect() as database_connection:
            user_update_query = update(Users).where(Users.id == self._service_parameters["user_id"]).values(is_active=False)
            result = database_connection.execute(user_update_query)
