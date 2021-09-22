# -*- encoding:utf-8 -*-
"""
                                                  - File description -
------------------------------------------------------------------------------------------------------------------------

"""
from db.connection import Session
from db.mapping.users import Users
from exception.users import UserNotFoundException
from logic import BaseServiceClass


class SignUp(BaseServiceClass):

    def __init__(self):
        super(SignUp, self).__init__()

    def execute(self) -> None:
        pass

    def validate_parameters(self) -> None:
        pass


class UserData:

    @staticmethod
    def retrieve_user_data(user: Users) -> dict:
        """Reads and returns the data of a given user"""
        """
        session = Session()
        user_data = {}

        try:
            user_data = session.query(Users).filter_by(id=user.id).all()
            if not user_data:
                raise UserNotFound()
        except:
            # TODO
            pass
        finally:
            session.close()

        return user_data
        """
