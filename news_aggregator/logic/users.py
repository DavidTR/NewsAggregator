# -*- encoding:utf-8 -*-
"""
                                                  - File description -
------------------------------------------------------------------------------------------------------------------------

"""
from typing import Any

from sqlalchemy.sql import select

from db.connection import database_engine
from db.mapping.rss_feeds import RSSFeeds
from db.mapping.users import Users, Subscriptions
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
        # TODO: Gestionar excepciones.

        user_data = subscriptions_data = None

        # TODO: Por Dios, implementar esto con relationships para que no sea necesario hacer tantas peticiones...
        #  Habrá que agregar relationships en users y en rss_feeds, para que subscriptions tenga acceso a los datos de
        #  usuarios y de los feeds de forma automática
        with database_engine.connect() as database_connection:
            user_data_query = select(Users.id, Users.name, Users.surname).where(Users.email == self._service_parameters["email"])
            user_data = database_connection.execute(user_data_query).first()
            # JOIN example.
            subscriptions_data_query = select(Users.id, RSSFeeds.title, RSSFeeds.url).join(Subscriptions, Subscriptions.user_id == Users.id).join(RSSFeeds, RSSFeeds.id == Subscriptions.rss_feed_id).where(Subscriptions.user_id == user_data.id)

            subscriptions_data = database_connection.execute(subscriptions_data_query).all()

        result = {
            "user_data": {
                "name": user_data.name,
                "surname": user_data.surname,
                "email": self._service_parameters["email"]
            },
            "subscriptions": [{"name": subscription.title, "url": subscription.url} for subscription in subscriptions_data]
        }

        print(result)
        return result


if __name__ == '__main__':

    instance = UserData()
    instance.set_parameters({"email": "test1@test.com"})
    instance.service_logic()
