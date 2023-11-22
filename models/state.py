#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
import models

class State(BaseModel, Base):
    """ State class """
    __tablename__ = 'states'  # Table name in the database
    name = Column(String(128), nullable=False)  # Column for the state name

    if models.FileStorage == 'db':
        # DBStorage relationship between State and City
        cities = relationship("City", backref="state", cascade="all, delete-orphan")
    else:
        # FileStorage relationship between State and City
        @property
        def cities(self):
            """Returns the list of City instances with state_id equal to the current State.id"""
            from models.city import City
            city_list = []
            for city in models.storage.all(City).values():
                if city.state_id == self.id:
                    city_list.append(city)
            return city_list
        