# -*- encoding:utf-8 -*-
"""
                                                  - File description -
------------------------------------------------------------------------------------------------------------------------

"""
from db.connection import Session
from db.mapping.users import Users
from exceptions.users import UserDataNotFound


class UserData:

    @staticmethod
    def retrieve_user_data(user: Users) -> dict:
        """Reads and returns the data of a given user"""

        session = Session()
        user_data = {}

        try:
            user_data = session.query(Users).filter_by(id=user.id)
        except:
            raise UserDataNotFound()
        finally:
            session.close()

        return user_data
