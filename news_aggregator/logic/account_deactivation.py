# -*- encoding:utf-8 -*-
"""
                                                  - File description -
------------------------------------------------------------------------------------------------------------------------
TODO: ¿Crear un nuevo archivo users.py y ubicar esta y otras clases de servicios relativos a usuarios ahí?.
"""

from sqlalchemy import select, update

from db.connection import database_engine
from db.mapping.users import Users
from exception.users import UserAccountDeactivated
from logic.base import BaseService
from util.meta import requires_login
from util.validators import is_integer_too_small, is_integer_too_large


@requires_login
class AccountDeactivation(BaseService):

    def __init__(self, *args, **kwargs):
        super(AccountDeactivation, self).__init__(*args, **kwargs)
        self._parameters_constraints = {
            "user_id": {
                "type": int,
                "validators": [
                    {
                        "function": is_integer_too_large,
                        "parameters": ["PARAMETER_VALUE", ]
                    },
                    {
                        "function": is_integer_too_small,
                        "parameters": ["PARAMETER_VALUE"]
                    }],
                "is_optional": False
            }
        }

    def _load_data(self) -> None:
        user_record_query = select(Users.is_active).where(Users.id == self._parameters["user_id"])

        with database_engine.connect() as database_connection:
            user_record = database_connection.execute(user_record_query).first()

        self._internal_data = {"user_record": user_record}

    def _preliminary_checks(self) -> None:

        # TODO: ¿Haría falta una comprobación por si los datos de usuario no se encontraran o esto ya lo cubre el
        #  login?. Creo que es así, login ya cubriría:
        #   - Existencia de registro de usuario.
        #   - Estado activo de la cuenta -> Un usuario desactivado podría seguir haciendo uso de su token por un
        #   tiempo limitado tras desactivar su cuenta. O bien hacemos esta comprobación o invalidamos su token.

        if not self._internal_data["user_record"].is_active:
            raise UserAccountDeactivated()

    def _execute(self) -> None:
        user_update_query = update(Users).where(Users.id == self._parameters["user_id"]).values(is_active=False)

        # Effectively deactivate the account.
        with database_engine.connect() as database_connection:
            database_connection.execute(user_update_query)


if __name__ == '__main__':
    instance = AccountDeactivation()
    instance.set_parameters({"user_id": 1})
    instance.validate_parameters()
    instance.service_logic()
