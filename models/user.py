#!/usr/bin/python3
"""This module defines a class User"""
from models.base_model import BaseModel, Base
import models
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

class User(BaseModel, Base):
    """This class defines a user by various attributes"""
    if models.storage_table == 'db':
        __tablename__ = 'users'
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128))
        last_name = Column(String(128))
        # Relationships for database storage
        places = relationship("Place", backref="user", cascade="all, delete-orphan")
        reviews = relationship("Review", backref="user", cascade="all, delete-orphan")
    else:
        email = ''
        password = ''
        first_name = ''
        last_name = ''
        # File storage doesn't use relationships, but you can define getters to simulate them
        # For example, to get all places of this user:
        @property
        def places(self):
            """Returns list of Place instances with user_id equals to the current User.id (FileStorage)"""
            place_list = []
            for place in models.storage.all("Place").values():
                if place.user_id == self.id:
                    place_list.append(place)
            return place_list

        @property
        def reviews(self):
            """Returns list of Review instances with user_id equals to the current User.id (FileStorage)"""
            review_list = []
            for review in models.storage.all("Review").values():
                if review.user_id == self.id:
                    review_list.append(review)
            return review_list

    def __init__(self, *args, **kwargs):
        """initializes the user"""
        super().__init__(*args, **kwargs)
