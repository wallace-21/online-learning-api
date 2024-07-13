#!/usr/bin/env python3

"""
    imports needed to run the program
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from database import Base
from datetime import datetime


class Assignment(Base):
    """
        Assignment model for representing assignments in the database.

        Attributes:
            id (int): The primary key identifier for the assignment.
            name (str): The name of the assignment.
            released_date (datetime): The release date of the assignment.
            due_date (datetime): The due date of the assignment.
            description (str): The description of the assignment.
    """
    __tablename__ = "assignment"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(length=100), nullable=False, unique=True)
    released_date = Column(DateTime, default=datetime.now)
    due_date = Column(DateTime, nullable=False)
    description = Column(Text, nullable=False)

    def __init__(self, name, released_date, due_date, description):
        """
            Initialize a new Assignment instance.
        """
        self.name = name
        self.released_date = released_date
        self.due_date = due_date
        self.description. description
