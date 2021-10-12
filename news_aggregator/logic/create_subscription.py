# -*- encoding:utf-8 -*-
"""
                                                  - File description -
------------------------------------------------------------------------------------------------------------------------

"""

from sqlalchemy import insert
from sqlalchemy.exc import IntegrityError

from db.connection import database_engine
from db.mapping.users import Subscriptions
from exception.rss_feeds import RSSFeedDoesNotExist
from exception.users import UserAlreadySubscribed
from logic.base import BaseService
from util.meta import requires_login
from util.validators import is_integer_too_large, is_integer_too_small


@requires_login
class CreateSubscription(BaseService):

    def __init__(self, *args, **kwargs):
        super(CreateSubscription, self).__init__(*args, **kwargs)
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
            "rss_feed_id": {
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

    def _execute(self) -> None:
        new_subscription_query = insert(Subscriptions).values(user_id=self._parameters["user_id"],
                                                              rss_feed_id=self._parameters["rss_feed_id"])
        # Check if the RSS feed exists and if user is already subscribed to the RSS feed. This time an EAFP approach is
        # used, as the database constraints will forbid duplicates (https://docs.python.org/3/glossary.html#term-eafp).
        with database_engine.connect() as database_connection:
            try:
                database_connection.execute(new_subscription_query)

            except IntegrityError as integrity_error:

                # Access to the original DBAPI exception code. See site-packages/MySQLdb/constants/ER.py
                internal_error_code = integrity_error.orig.args[0]
                if internal_error_code == 1452:
                    self._logger.error(f"The RSS feed does not exist: {integrity_error}")
                    raise RSSFeedDoesNotExist()
                elif internal_error_code == 1062:
                    self._logger.error(f"The user is already subscribed to the RSS feed: {integrity_error}")
                    raise UserAlreadySubscribed()


if __name__ == '__main__':
    instance = CreateSubscription()
    instance.set_parameters({"user_id": 1, "rss_feed_id": 1})
    instance.validate_parameters()
    print(instance.service_logic())
