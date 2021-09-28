# -*- encoding:utf-8 -*-
"""
                                                  - File description -
------------------------------------------------------------------------------------------------------------------------

"""
from db.mapping.users import Users


class UserData:

    def __init__(self, *args, **kwargs):
        super(UserData, self).__init__()
        self._service_parameters_constraints = {

        }

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
