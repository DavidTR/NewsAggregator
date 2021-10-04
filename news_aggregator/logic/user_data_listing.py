# -*- encoding:utf-8 -*-
"""
                                                  - File description -
------------------------------------------------------------------------------------------------------------------------

"""
from typing import Any, Tuple

from sqlalchemy.sql import select

from db.connection import database_engine
from db.mapping.rss_feeds import RSSFeeds
from db.mapping.users import Users, Subscriptions
from exception.users import UserNotFound
from logic.base import BaseService
from util.validators import is_integer_too_small, is_integer_too_large


class UserDataListing(BaseService):

    def __init__(self, *args, **kwargs):
        super(UserDataListing, self).__init__(*args, **kwargs)
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
            }
        }

    def _load_data(self) -> None:
        # TODO: Por Dios, implementar esto con relationships para que no sea necesario hacer tantas peticiones...
        #  Habrá que agregar relationships en users y en rss_feeds, para que subscriptions tenga acceso a los datos de
        #  usuarios y de los feeds de forma automática

        with database_engine.connect() as database_connection:
            user_data_query = select(Users.id, Users.name, Users.surname, Users.email) \
                .where(Users.id == self._parameters["user_id"])
            user_data = database_connection.execute(user_data_query).first()

            # TODO: ¿Haría falta una comprobación por si los datos de usuario no se encontraran o esto ya lo cubre el
            #  login?. Creo que es así, login ya cubriría:
            #   - Existencia de registro de usuario.
            #   - Estado activo de la cuenta.

            subscriptions_data_query = select(Users.id, RSSFeeds.title, RSSFeeds.url).\
                join(Subscriptions, Subscriptions.user_id == Users.id).\
                join(RSSFeeds, RSSFeeds.id == Subscriptions.rss_feed_id).where(Subscriptions.user_id == user_data.id)

            subscriptions_data = database_connection.execute(subscriptions_data_query).all()

        # TODO: Encontrar mejor manera de pasar datos entre métodos internos, por parámetro no es lo adecuado.
        self._internal_data = {"user_data": user_data, "subscriptions_data": subscriptions_data}

    def _build_response(self) -> dict:

        # Prepare the data and give it a specific format for the response.
        user_data = self._internal_data["user_data"]
        subscriptions_data = self._internal_data["subscriptions_data"]

        result = {
            "user_data": {
                "name": user_data.name,
                "surname": user_data.surname,
                "email": user_data.email
            },
            "subscriptions": {}
        }

        if subscriptions_data:
            result["subscriptions"] = [{"name": subscription.title, "url": subscription.url}
                                       for subscription in subscriptions_data]

        return result
