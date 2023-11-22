#!/usr/bin/python3
""" City Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey

class City(BaseModel, Base):
    """ The city class, contains state ID and name """
    __tablename__ = 'cities'  # Table name in the database
    name = Column(String(128), nullable=False)  # Column for the city name
    state_id = Column(String(60), ForeignKey('states.id'), nullable=False)  # Column for the state_id