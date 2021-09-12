# -*- encoding:utf-8 -*-
"""
                                                  - File description -
------------------------------------------------------------------------------------------------------------------------
Database connection engine. As only one engine should be created, a "singleton" pattern is used.

"""
from util import design_patterns
from sqlalchemy import create_engine


class DatabaseEngine(metaclass=design_patterns.SingletonMetaclass):
    pass
