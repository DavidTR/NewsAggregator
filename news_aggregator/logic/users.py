# -*- encoding:utf-8 -*-
"""
                                                  - File description -
------------------------------------------------------------------------------------------------------------------------

"""
from db.mapping.users import Users
from logic.base import BaseServiceClass
from util.validators import has_minimum_length, email_format_validator, has_minimum_capital_letters, \
    contains_special_characters


class SignUp(BaseServiceClass):

    def __init__(self):
        super(SignUp, self).__init__()
        self._service_parameters_constraints = {
            "name": {
                "type": str,
                "validators": [
                    {
                        "function": has_minimum_length,
                        "parameters": ["PARAMETER_VALUE", 25]
                    }
                ],
                "is_optional": False
            },
            "surname": {
                "type": str,
                "validators": [
                    {
                        "function": has_minimum_length,
                        "parameters": ["PARAMETER_VALUE", 40]
                    }
                ],
                "is_optional": False
            },
            "email": {
                "type": str,
                "validators": [
                    {
                        "function": email_format_validator,
                        "parameters": ["PARAMETER_VALUE"]
                    }
                ],
                "is_optional": False
            },
            "password": {
                "type": str,
                "validators": [
                    {
                        "function": has_minimum_length,
                        "parameters": ["PARAMETER_VALUE", 8]
                    },
                    {
                        "function": has_minimum_capital_letters,
                        "parameters": ["PARAMETER_VALUE"]
                    },
                    {
                        "function": contains_special_characters,
                        "parameters": ["PARAMETER_VALUE"]
                    },
                ],
                "is_optional": False
            }
        }

    def execute(self) -> None:
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
