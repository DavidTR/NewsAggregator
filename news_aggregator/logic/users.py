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


class UserData(BaseService):

    def __init__(self, *args, **kwargs):
        super(UserData, self).__init__(*args, **kwargs)
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

    def prepare(self) -> Tuple[dict, dict]:
        # TODO: Por Dios, implementar esto con relationships para que no sea necesario hacer tantas peticiones...
        #  Habrá que agregar relationships en users y en rss_feeds, para que subscriptions tenga acceso a los datos de
        #  usuarios y de los feeds de forma automática

        with database_engine.connect() as database_connection:
            user_data_query = select(Users.id, Users.name, Users.surname, Users.email) \
                .where(Users.id == self._service_parameters["user_id"])
            user_data = database_connection.execute(user_data_query).first()

            # If there's no user data (e.g., the user does not exist), the process is aborted. This exception should
            # never be raised, as the previous login should have checked this condition.
            if not user_data:
                raise UserNotFound()

            subscriptions_data_query = select(Users.id, RSSFeeds.title, RSSFeeds.url).join(Subscriptions,
                                                                                           Subscriptions.user_id == Users.id).join(
                RSSFeeds, RSSFeeds.id == Subscriptions.rss_feed_id).where(Subscriptions.user_id == user_data.id)

            subscriptions_data = database_connection.execute(subscriptions_data_query).all()

        return user_data, subscriptions_data

    def preliminary_checks(self, *args) -> Any:
        # No preliminary checks needed.
        pass

    def service_logic(self, user_data, subscriptions_data) -> dict:

        # Prepare the data and give it a specific format for the response.
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


if __name__ == '__main__':
    instance = UserData()
    instance.set_parameters({"user_id": 3})
    instance.validate_parameters()
    service_data = instance.prepare()
    print(instance.service_logic(*service_data))
