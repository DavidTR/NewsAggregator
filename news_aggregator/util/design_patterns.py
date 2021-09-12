# -*- encoding:utf-8 -*-
"""
                                                  - File description -
------------------------------------------------------------------------------------------------------------------------
Implementations of design patterns used in the application.

"""


class SingletonMetaclass(type):
    """Singleton creation pattern metaclass implementation"""

    # This data structure will ensure that only one instance of a given class is created and stored at a time.
    # This is a class level private static attribute, as it's defined in the class scope and not inside a method.
    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        In metaclasses, this method is executed before __new__ and __init__ for instance creation of the classes that
        have this class as their metaclass. This method should call __new__ and __init__ so as to follow the usual
        instance creation method in Python (here is done in the line super(Singleton, cls).__call__(*args, **kwargs)).

        As this is a metaclass implementation of the Singleton pattern, whenever a new class tries to create a new
        instance, the existing instance should be returned or created if it didn't exist. This method ensures that
        this behaviour is implemented correctly.
        """
        if cls.__name__ not in cls._instances:
            cls._instances[cls.__name__] = super(SingletonMetaclass, cls).__call__(*args, **kwargs)
        return cls._instances[cls.__name__]
