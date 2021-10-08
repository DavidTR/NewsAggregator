# -*- encoding:utf-8 -*-
"""
                                                  - File description -
------------------------------------------------------------------------------------------------------------------------

"""

from sqlalchemy.sql import delete, select

from db.connection import database_engine
from db.mapping.rss_feeds import RSSFeeds
from db.mapping.users import Subscriptions
from exception.rss_feeds import RSSFeedDoesNotExist
from exception.subscriptions import SubscriptionDoesNotExist
from logic.base import BaseService
from util.validators import is_integer_too_large, is_integer_too_small


class DeleteSubscription(BaseService):

    def __init__(self, *args, **kwargs):
        super(DeleteSubscription, self).__init__(*args, **kwargs)
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

    def _load_data(self) -> None:

        # Load the subscription from the database to check if it exists.
        subscription_query = select(Subscriptions). \
            where(Subscriptions.user_id == self._parameters["user_id"]). \
            where(Subscriptions.rss_feed_id == self._parameters["rss_feed_id"])

        rss_feed_query = select(RSSFeeds).\
            where(RSSFeeds.id == self._parameters["rss_feed_id"])

        with database_engine.connect() as database_connection:
            subscription_record = database_connection.execute(subscription_query)
            rss_feed_record = database_connection.execute(rss_feed_query)

        self._internal_data = {"subscription_record": subscription_record, "rss_feed_record": rss_feed_record}

    def _preliminary_checks(self) -> None:

        # If the RSS feed does not exist, an exception is raised.
        if self._internal_data["rss_feed_record"].rowcount == 0:
            raise RSSFeedDoesNotExist()

        # If the subscription could not be found, an exception is raised.
        if self._internal_data["subscription_record"].rowcount == 0:
            raise SubscriptionDoesNotExist()

    def _execute(self) -> None:

        # Effectively delete the subscription.
        with database_engine.connect() as database_connection:
            subscription_deletion_query = delete(Subscriptions). \
                where(Subscriptions.user_id == self._parameters["user_id"]). \
                where(Subscriptions.rss_feed_id == self._parameters["rss_feed_id"])
            database_connection.execute(subscription_deletion_query)

    def _build_response(self) -> dict:
        return {"message": "Subscription deleted successfully"}


if __name__ == '__main__':
    instance = DeleteSubscription()
    instance.set_parameters({"user_id": 1, "rss_feed_id": 1})
    instance.validate_parameters()
    print(instance.service_logic())

