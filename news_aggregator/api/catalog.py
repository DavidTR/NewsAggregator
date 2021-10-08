# -*- encoding:utf-8 -*-
"""
                                                  - File description -
------------------------------------------------------------------------------------------------------------------------

"""
from typing import Tuple

from tornado.httputil import HTTPServerRequest

from api.base import APIRequestProcessor
from logic.get_rss_catalog import GetRSSCatalog


class CatalogProcessor(APIRequestProcessor):

    def get_rss_catalog(self, request: HTTPServerRequest) -> Tuple[int, dict]:
        return self.process_request(request, GetRSSCatalog, are_querystring_args_allowed=True)
