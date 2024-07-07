#!/bin/python3

"""
    imports that are necessary for the program
"""
from sqlalchemy import Column, Integer, String, DateTime
from database import Base
from datetime import datetime


class Lecture(Base):
    """
        Lecture model for representing lectures in the database.

        Attributes:
            id (int): The primary key identifier for the lecture.
            name (str): The name of the lecture.
            date_and_time (datetime): The date and time of the lecture.
            mentors (str): The names of the mentors for the lecture.
    """
    __tablename__ = "lecture"

    id = Column(Integer, nullable=False, primary_key=True)
    name = Column(String(length=50), nullable=False, unique=True)
    date_and_time = Column(DateTime, nullable=False)
    mentors = Column(String(length=50), nullable=False)

    def __init__(self, id, date_and_time, mentors):
        """
            Initialize a new Lecture instance
        """
        self.id = id
        self.name = name
        self.date_and_time = date_and_time
        self.mentors = mentors
