#!/usr/bin/python3
"""This module instantiates an object of class FileStorage"""

from os import getenv

# List of models to be imported when using wildcard import
__all__ = ["BaseModel", "User", "State", "City", "Amenity", "Place", "Review", "storage"]

storage_table = getenv("HBNB_TYPE_STORAGE")

if storage_table == "db":
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
else:
    from models.engine.file_storage import FileStorage
    storage = FileStorage()

# Import model classes
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review

storage.reload()
