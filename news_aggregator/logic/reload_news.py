# -*- encoding:utf-8 -*-
"""
                                                  - File description -
------------------------------------------------------------------------------------------------------------------------

"""
import time
from datetime import datetime
from typing import Union

from sqlalchemy.sql import select
from tornado.gen import multi
from tornado.httpclient import AsyncHTTPClient

from db.connection import database_engine
from db.mapping.rss_feeds import RSSFeeds
from db.mapping.users import Subscriptions
from exception.users import UserHasNoSubscriptions
from logic.base import BaseService
from util.util import fast_list_flattener
from util.validators import is_integer_too_large, is_integer_too_small

# TODO: CONTINUAR


class ReloadNews(BaseService):

    def __init__(self, *args, **kwargs):
        super(ReloadNews, self).__init__(*args, **kwargs)

        # This service
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
        # TODO: Incluir relationships para que no sea necesario cargar los datos por separado.
        user_subscriptions_query = select(Subscriptions.rss_feed_id).where(
            Subscriptions.user_id == self._parameters["user_id"])

        with database_engine.connect() as database_connection:
            user_subscriptions = database_connection.execute(user_subscriptions_query).all()

            flattened_subscriptions_ids = fast_list_flattener(user_subscriptions)

            user_rss_feeds_query = select(RSSFeeds.id, RSSFeeds.title, RSSFeeds.url, RSSFeeds.last_update_date). \
                where(RSSFeeds.id.in_(flattened_subscriptions_ids))

            user_rss_feeds = database_connection.execute(user_rss_feeds_query).all()

        self._internal_data = {"user_rss_feeds": user_rss_feeds}

    def _preliminary_checks(self) -> None:

        if len(self._internal_data["user_rss_feeds"]) == 0:
            raise UserHasNoSubscriptions()

    async def _fetch_rss_news(self):

        async_http_client = AsyncHTTPClient()

        # TODO: ¿Es necesario todo esto? Estudiar mejor asyncio.
        async def _labelled_rss_fetch(rss_feed):
            return rss_feed.id, await async_http_client.fetch(rss_feed.url)

        # TODO: Las dos alternativas son las siguientes:
        #  - labelled_rss_fetch + results[response[0]] = await response[1].text()
        #  - task_list.append(async_http_requests_client.get(rss_feed.url)) + results[response.url] = await response.text()
        def _get_tasks() -> list:
            """Construct a list of coroutine tasks to fetch RSS news asynchronously"""
            task_list = []
            for rss_feed in self._internal_data["user_rss_feeds"]:
                # RSS feeds will only be updated
                # TODO: Agregar soporte para eTag.
                if rss_feed.updated_date <= datetime.now():
                    task_list.append(_labelled_rss_fetch(rss_feed))

            return task_list

        # TODO: Explicar y testear -> Añadir más sitios RSS y medir tiempos entre una alternativa y otra.
        """
        async with aiohttp.ClientSession() as async_http_requests_client:
            responses = await asyncio.gather(*_get_tasks())
            for response in responses:
                results[response[0]] = await response[1].text()
        """
        results = await multi(_get_tasks())

        return results

    def _execute(self):

        # Use asyncio and uvloop for a more efficient way to fetch and store the data.
        # TODO: Testear uvloop, agregar más RSS para poder comparar.
        # asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
        start_time = time.time()
        # IOLoop.current().add_future(run_in_stack_context(NullContext(), self._fetch_rss_news),
        #                             lambda f: f.result())
        self._internal_data["updated_rss_news"] = self._fetch_rss_news()
        print(time.time() - start_time)

    def _post_execute(self) -> None:
        # Update the database with the freshly fetched news.
        pass

    def _build_response(self) -> Union[dict, list]:
        pass


if __name__ == '__main__':
    instance = ReloadNews()
    instance.set_parameters({"user_id": 1})
    instance.validate_parameters()
    print(instance.service_logic())
