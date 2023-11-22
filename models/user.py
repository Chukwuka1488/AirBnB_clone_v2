#!/usr/bin/python3
"""This module defines a class User"""
from models.base_model import BaseModel, Base
import models
from os import getenv
import sqlalchemy
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
        # Relationship with Place
        places = relationship("Place", backref="user", cascade="all, delete")
        reviews = relationship("Review", backref="user", cascade="all, delete")
    else:
        email = ''
        password = ''
        first_name = ''
        last_name = ''


    def __init__(self, *args, **kwargs):
        """initializes the user"""
        super().__init__(*args, **kwargs)