# -*- encoding:utf-8 -*-
"""
                                                  - File description -
------------------------------------------------------------------------------------------------------------------------


TODO: ¿Se puede incluir en el mensaje de error el nombre de los campos que no pasen las validaciones de forma elegante?
TODO: ¿Incluir más información sobre el error (número de caracteres o mayúsculas requeridos, etc...).? NO INCURRIR EN
      DAR DEMASIADA INFORMACION.
"""
import re
import string

from const.data import MAX_INT_VALUE, MIN_INT_VALUE
from exception.validation import IncorrectFormat, InsufficientLength, NotEnoughCapitalLetters, \
    NotEnoughSpecialCharacters, MaxLengthExceeded, IntegerTooLarge, IntegerTooSmall


def is_valid_email(email: str) -> None:
    """Checks if the given email is valid"""
    email_regex = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")

    # "fullmatch" checks if the whole string matches the regular expression, better fit for this function than "match".
    if not isinstance(email, str) or not email_regex.fullmatch(email):
        raise IncorrectFormat(formatting_data={"name": "email"})


def has_minimum_length(test_string: str, min_length: int = 8) -> None:
    """Checks if the given password has 'max_length' characters minimum"""
    if not isinstance(test_string, str) or len(test_string) < min_length:
        raise InsufficientLength()


def surpasses_maximum_length(test_string: str, max_length: int = 8) -> None:
    """Checks if the given password has 'max_length' characters maximum"""
    if not isinstance(test_string, str) or len(test_string) > max_length:
        raise MaxLengthExceeded()


def has_minimum_capital_letters(test_string: str,  min_capital_letters: int = 2) -> None:
    """Checks if the given password has at least one capital letter"""
    if not isinstance(test_string, str) or sum(map(str.isupper, test_string)) < min_capital_letters:
        raise NotEnoughCapitalLetters()


def contains_special_characters(test_string: str, min_special_characters: int = 3) -> None:
    """Checks if the password has a minimum number of special, punctuation characters"""
    password_special_characters = sum([character in test_string for character in list(string.punctuation)])

    if not isinstance(test_string, str) or password_special_characters < min_special_characters:
        raise NotEnoughSpecialCharacters()


def is_integer_too_large(integer_value: int) -> None:
    """Checks if the integer value is too large to be supported"""

    # MAX_INT_VALUE is not supported either.
    if integer_value >= MAX_INT_VALUE:
        raise IntegerTooLarge()


def is_integer_too_small(integer_value: int) -> None:
    """Checks if the integer value is too small to be supported"""

    # MIN_INT_VALUE is not supported either.
    if integer_value <= MIN_INT_VALUE:
        raise IntegerTooSmall()
