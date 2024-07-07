#!/usr/bin/python3

"""
    imports necessary for the program
"""
from sqlalchemy import Column, String, Integer, Boolean, DateTime
from database import Base
from datetime import datetime


class User(Base):
    """
        User model for representing users in the database.

        Attributes:
            id (str): The primary key identifier for the user.
            name (str): The first name of the user.
            surname (str): The surname of the user.
            instructor (bool): Whether the user is an instructor.
            nationality (str): The nationality of the user.
            email (str): The email address of the user.
            password (str): The password of the user.
            date_created (datetime): The date and time when the
                                     user was created.
    """
    __tablename__ = 'users'

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    instructor = Column(Boolean, default=False)
    nationality = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    date_created = Column(DateTime, default=datetime.utcnow)

    def __init__(self, id, name, surname, instructor, nationality,
                 email, password):
        """
            Initialize a new User instance.
        """
        self.id = id
        self.name = name
        self.surname = surname
        self.instructor = instructor
        self.nationality = nationality
        self.email = email
        self.password = password
