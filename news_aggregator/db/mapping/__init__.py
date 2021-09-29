# -*- encoding:utf-8 -*-
"""
                                                  - File description -
------------------------------------------------------------------------------------------------------------------------
This module will hold all the mapping classes needed by the ORM in order to operate the database tables.

Each file will keep a certain number of classes that will be related mainly to the name of the module.
For example, in the "users" file, mapping classes for tables such as "users", "sessions" or "users_rss_feeds" cam be
found, all of them having in common that the users are the part with the most importance in their purpose.

"""
# TODO: Mover a nuevo módulo base.py por consistencia.
from sqlalchemy.orm import declarative_base

# This class will be used in all the mapping classes as their parent class. It will be declared only once, and imported
# from this file.
MappingBaseClass = declarative_base()
