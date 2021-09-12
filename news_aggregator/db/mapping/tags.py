# -*- encoding:utf-8 -*-
"""
                                                  - File description -
------------------------------------------------------------------------------------------------------------------------
Mapping classes for tags-oriented tables. See db/mapping/__init__.py for more information.

"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, JSON

from db.mapping import MappingBaseClass


class Tags(MappingBaseClass):
    """"""
    __tablename__ = "tags"

    id = Column(Integer, autoincrement=True, primary_key=True)
    title = Column(String(50), nullable=False)
    description = Column(String(200))

