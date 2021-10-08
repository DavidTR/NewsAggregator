# -*- encoding:utf-8 -*-
"""
                                                  - File description -
------------------------------------------------------------------------------------------------------------------------

"""
from typing import Union

from sqlalchemy.sql import select

from db.connection import database_engine
from db.mapping.rss_feeds import RSSFeeds, RSSFeedsTags
from logic.base import BaseService
from util.util import fast_list_flattener
from util.validators import is_integer_too_large, is_integer_too_small


class GetRSSCatalog(BaseService):

    def __init__(self, *args, **kwargs):
        super(GetRSSCatalog, self).__init__(*args, **kwargs)

        # This service
        self._parameters_constraints = {
            "tag_id": {
                "type": int,
                "validators": [
                    {
                        "function": is_integer_too_large,
                        "parameters": ["PARAMETER_VALUE"]
                    },
                    {
                        "function": is_integer_too_small,
                        "parameters": ["PARAMETER_VALUE"]
                    }
                ],
                "is_optional": True
            }
        }

    def _load_data(self) -> None:

        rss_feeds_query = select(RSSFeeds).order_by(RSSFeeds.id)

        if "tag_id" in self._parameters:
            tagged_rss_feeds_query = select(RSSFeedsTags.rss_feed_id).where(RSSFeedsTags.tag_id == self._parameters["tag_id"])

            with database_engine.connect() as database_connection:
                tagged_rss_feeds = database_connection.execute(tagged_rss_feeds_query).all()
                tagged_rss_feeds_ids = fast_list_flattener(tagged_rss_feeds)

            rss_feeds_query = select(RSSFeeds).where(RSSFeeds.id.in_(tagged_rss_feeds_ids)).order_by(RSSFeeds.id)

        with database_engine.connect() as database_connection:
            rss_feeds = database_connection.execute(rss_feeds_query).all()

        self._internal_data = {"rss_feeds": rss_feeds}

    def _build_response(self) -> Union[dict, list]:

        result = []

        for rss_feed in self._internal_data["rss_feeds"]:
            rss_feed_output_data = {
                "title": rss_feed.title,
                "url": rss_feed.url
            }
            result.append(rss_feed_output_data)

        return result


if __name__ == '__main__':
    instance = GetRSSCatalog()
    instance.set_parameters({"tag_id": 1})
    instance.validate_parameters()
    print(instance.service_logic())
