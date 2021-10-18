# -*- encoding:utf-8 -*-
"""
                                                  - File description -
------------------------------------------------------------------------------------------------------------------------
TODO: Documentar: Recibe una lista que comprende el nuevo orden de todos y cada uno de los feeds RSS a los que está
 suscrito el usuario. No se aceptan ordenamientos parciales. No se aceptan valores de orden repetidos.
"""

from sqlalchemy import select, update

from db.connection import database_engine, Session
from db.mapping.users import Subscriptions
from exception.subscriptions import NewOrderListIncorrectLength, MalformedNewOrderList, InvalidRSSFeedInNewOrderList, \
    InvalidOrderValueInNewOrderList
from exception.users import UserHasNoSubscriptions
from logic.base import BaseService
from util.meta import requires_login
from util.validators import is_integer_too_large, is_integer_too_small


@requires_login
class ReorderSubscriptions(BaseService):

    def __init__(self, *args, **kwargs):
        super(ReorderSubscriptions, self).__init__(*args, **kwargs)
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
            "new_order": {
                "type": list,
                "validators": [],
                "is_optional": False
            }
        }

    def _load_data(self) -> None:

        user_subscriptions_query = select(Subscriptions.user_id, Subscriptions.rss_feed_id,
                                          Subscriptions.subscription_order). \
            where(Subscriptions.user_id == self._parameters["user_id"])

        with database_engine.connect() as database_connection:
            user_subscriptions = database_connection.execute(user_subscriptions_query).all()

        self._internal_data = {"user_subscriptions": user_subscriptions}

    def _preliminary_checks(self) -> None:

        user_subscriptions = self._internal_data["user_subscriptions"]

        if not user_subscriptions:
            raise UserHasNoSubscriptions()

        if len(self._parameters["new_order"]) != len(user_subscriptions):
            raise NewOrderListIncorrectLength()

        user_rss_ids = [subscription.rss_feed_id for subscription in user_subscriptions]
        allowed_order_values = list(range(1, len(user_rss_ids) + 1))

        for order_dict in self._parameters["new_order"]:
            if not isinstance(order_dict, dict) or order_dict.keys() != {"rss_feed_id", "new_order"}:
                raise MalformedNewOrderList()

            if order_dict["rss_feed_id"] not in user_rss_ids:
                raise InvalidRSSFeedInNewOrderList()

            if order_dict["new_order"] not in allowed_order_values:
                raise InvalidOrderValueInNewOrderList(formatting_data={"allowed_order_values": allowed_order_values})

    def _execute(self) -> None:

        new_order = self._parameters["new_order"]
        user_subscriptions = self._internal_data["user_subscriptions"]

        def _get_current_order(rss_feed_id: int):
            """
            Returns the current order (in database) of a given subscription's RSS feed ID.
            Encapsulated for clarity
            """
            for subscription in user_subscriptions:
                if subscription.rss_feed_id == rss_feed_id:
                    return subscription.subscription_order

        # TODO: No me gusta mucho la idea pero, ¿se ganaría algo haciéndolo de forma asíncrona?.
        with Session() as session:
            for order in new_order:
                current_order = _get_current_order(order["rss_feed_id"])

                # Avoid executing the database query if it's not necessary.
                if current_order == order["new_order"]:
                    continue

                subscription_order_update_query = update(Subscriptions).where(
                    Subscriptions.user_id == self._parameters["user_id"]).where(
                    Subscriptions.rss_feed_id == order["rss_feed_id"]).values(subscription_order=order["new_order"])

                session.execute(subscription_order_update_query)

            session.commit()


if __name__ == '__main__':
    instance = ReorderSubscriptions()
    instance.set_parameters({"user_id": 1, "new_order": [{"new_order": 1, "rss_feed_id": 1},
                                                         {"rss_feed_id": 2, "new_order": 1}]})
    instance.validate_parameters()
    print(instance.service_logic())
