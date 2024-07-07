#!/usr/bin/python3

"""
    imports necessary for the program
"""
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text
from database import Base


class Course(Base):
    """
        Course model for representing courses in the database.

        Attributes:
            id (int): The primary key identifier for the course.
            name (str): The name of the course.
            price (int): The price of the course.
            duration (str): The duration of the course.
            description (str): The description of the course.
            certification (bool): Whether the course provides certification.
    """
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(length=50), nullable=False, index=True, unique=True)
    price = Column(Integer, nullable=True)
    duration = Column(String(length=25), nullable=False)
    description = Column(Text, nullable=True)
    certifaction = Column(Boolean, nullable=False)

    def __init__(self, id, name, price, description, certification):
        """
            Initialize a new Course instance
        """
        self.id = id
        self.name = name
        self.price = price
        self.description = description
        self.certification = certification
