# -*- encoding:utf-8 -*-
"""
                                                  - File description -
------------------------------------------------------------------------------------------------------------------------

"""
import concurrent.futures
import datetime
import time
from typing import Union

import requests
from lxml import etree
from lxml.etree import XMLSyntaxError
from sqlalchemy import update
from sqlalchemy.sql import select
from tornado.gen import multi
from tornado.httpclient import AsyncHTTPClient

from cfg import config
from db.connection import database_engine, Session
from db.mapping.rss_feeds import RSSFeeds, RSSFeedsNews
from db.mapping.users import Subscriptions
from exception.users import UserHasNoSubscriptions
from logic.base import BaseService
from util.util import fast_list_flattener
from util.validators import is_integer_too_large, is_integer_too_small


# TODO: CONTINUAR


# @requires_login
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

        # This data structure will hold the revised user RSS feeds, i.e., all RSS feeds classified in one of two
        # categories: The ones that need to be refreshed by fetching new data from their URL and the ones that will
        # return their cached news, stored in the database.
        filtered_user_rss_feeds = {"from_cache": [], "url_fetch": []}
        rss_cache_time = datetime.datetime.now() + datetime.timedelta(minutes=config.settings.RSS_CACHE_MINUTES)

        for rss_feed in self._internal_data["user_rss_feeds"]:
            revised_rss_feed = {
                "db_record_id": rss_feed.id,
                "url": rss_feed.url
            }

            if not rss_feed.last_update_date or rss_feed.last_update_date >= rss_cache_time:
                filtered_user_rss_feeds["url_fetch"].append(revised_rss_feed)
            else:
                filtered_user_rss_feeds["from_cache"].append(revised_rss_feed)

        self._internal_data["filtered_user_rss_feeds"] = filtered_user_rss_feeds

    async def _fetch_rss_news(self):

        async_http_client = AsyncHTTPClient()

        # TODO: ¿Es necesario todo esto? Estudiar mejor asyncio.
        async def _labelled_rss_fetch(rss_feed):
            return rss_feed.id, await async_http_client.fetch(rss_feed.url)

        def _get_tasks() -> list:
            """Construct a list of coroutine tasks to fetch RSS news asynchronously"""
            task_list = []
            for rss_feed in self._internal_data["filtered_user_rss_feeds"]["url_fetch"]:
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

    def _threaded_rss_news_fetch(self):
        """Retrieves the news from the loaded URLs using threads"""

        def sync_rss_feed_fetch(url_address: str, timeout_seconds: int = 10):
            """Fetches a RSS feed synchronously"""
            return requests.get(url_address, timeout=timeout_seconds)

        # Context manager that will wait for all the threads to finish. Optionally, an upper limit for max_workers
        # can be set.
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as threaded_executor:

            # First, prepare the list of futures and gather them in a dictionary to be resolved later.
            # A dict comprehension won't be used for readability purposes.
            rss_news_futures = {}
            for filtered_user_rss_feed in self._internal_data["filtered_user_rss_feeds"]["url_fetch"]:
                rss_news_futures[threaded_executor.submit(sync_rss_feed_fetch, filtered_user_rss_feed["url"], 20)] = filtered_user_rss_feed

            # Resolve the futures and save the data required in latter operations.
            # concurrent.futures.as_completed spawns the threads that effectively perform the URL fetch and waits for
            # each call to complete so we can handle the results.
            for future in concurrent.futures.as_completed(rss_news_futures):

                try:
                    rss_data = rss_news_futures[future]

                    # Update the internal revised RSS data with the complete HTTP response.
                    rss_data["http_response"] = future.result()
                except Exception as resolve_exception:
                    self._logger.error(f"An error occurred when resolving the future for the URL: "
                                       f"{resolve_exception}. The RSS feed won't be updated")

    # Implementación con multiprocessing.
    # Implementación con hebras clásicas.
    # https://stackoverflow.com/questionsx/2632520/what-is-the-fastest-way-to-send-100-000-http-requests-in-python#comment107423317_46144596
    # Benchmarks para cada una de las soluciones, comparar cuál de ellas es la mejor.

    def _retrieve_rss_records_from_database(self):
        """Retrieves the database news for those sites that are not outdated"""

        with database_engine.connect() as database_connection:

            for filtered_user_rss_feed in self._internal_data["filtered_user_rss_feeds"]["from_cache"]:
                cached_rss_record_query = select(RSSFeedsNews).\
                    where(RSSFeedsNews.rss_feed_id == filtered_user_rss_feed["db_record_id"]).\
                    order_by(RSSFeedsNews.id.desc())

                cached_rss_record = database_connection.execute(cached_rss_record_query).first()
                filtered_user_rss_feed["xml_raw_data"] = cached_rss_record.news_data

    def _execute(self):

        # Use asyncio and uvloop for a more efficient way to fetch and store the data.
        # TODO: Testear uvloop, agregar más RSS para poder comparar.
        # asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
        start_time = time.time()
        # IOLoop.current().add_future(run_in_stack_context(NullContext(), self._fetch_rss_news),
        #                             lambda f: f.result())
        # Fetch new data for those RSS sites that are outdated.
        self._threaded_rss_news_fetch()

        # And retrieve database records from the database for those that are not.
        self._retrieve_rss_records_from_database()

        print(time.time() - start_time)

    def _post_execute(self) -> None:

        # Once the data has been retrieved, check if it every XML is well formed and update the database.

        # Objects to be bulk-inserted in the database. Bulk operations are more efficient as they save some of the
        # overhead produced by the unit-of-work pattern.
        # See: https://docs.sqlalchemy.org/en/14/orm/persistence_techniques.html#bulk-operations
        new_db_rss_news_records = []
        rss_feeds_update_queries = []

        for filtered_user_rss_feed in self._internal_data["filtered_user_rss_feeds"]["url_fetch"]:

            site_response = filtered_user_rss_feed["http_response"]

            # Check if the remote call finished with a 200 status and if it has the data we need in the required
            # format. If any of these conditions are not met, the RSS feed will be ignored and it won't be
            # updated.
            if site_response.status_code == 200:
                xml_raw_data = site_response.content
                try:
                    # Checks parse errors.
                    etree.fromstring(xml_raw_data)

                    new_db_rss_news_records.append(RSSFeedsNews(rss_feed_id=filtered_user_rss_feed["db_record_id"],
                                                                query_date=datetime.datetime.now(),
                                                                news_data=xml_raw_data))

                    rss_feeds_update_queries.append(update(RSSFeeds).
                                                    where(RSSFeeds.id == filtered_user_rss_feed["db_record_id"]).
                                                    values(last_update_date=datetime.datetime.now()))

                    # After checking that the data is valid, update the internal data record to return it in the
                    # service's response. The response is decoded as an UTF-8 string to match the response format.
                    filtered_user_rss_feed["xml_raw_data"] = str(xml_raw_data, 'utf-8')

                except XMLSyntaxError as xml_parse_error:
                    self._logger.error(f"The XML data for the URL {filtered_user_rss_feed['url']}: {xml_parse_error}, "
                                       f"continuing...")

        # Finally, save the records in the database.
        with Session() as session:
            session.bulk_save_objects(new_db_rss_news_records)

            # And update the last_updated_date value for the RSS feed record.
            for query in rss_feeds_update_queries:
                session.execute(query)

            session.commit()

    def _build_response(self) -> Union[dict, list]:

        response = []

        # Mix both dictionaries to build the response.
        # This copy is not entirely necessary
        all_updated_rss_data = self._internal_data["filtered_user_rss_feeds"]["url_fetch"]
        all_updated_rss_data.extend(self._internal_data["filtered_user_rss_feeds"]["from_cache"])

        # Return the XML data retrieved from the RSS sites.
        for revised_user_rss_feed in all_updated_rss_data:
            fresh_rss_response = {
                "url": revised_user_rss_feed["url"],
                "data": revised_user_rss_feed["xml_raw_data"]
            }

            response.append(fresh_rss_response)

        return response


if __name__ == '__main__':
    instance = ReloadNews()
    instance.set_parameters({"user_id": 1})
    instance.validate_parameters()
    print(instance.service_logic())
