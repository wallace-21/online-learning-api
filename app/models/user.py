#!/usr/bin/python3

"""
    imports necessary for the program
"""
from sqlalchemy import Column, String, Integer, Boolean, DateTime
from database import Base
from datetime import datetime

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(length=80), unique=True, nullable=False)
    password = Column(String(length=200), nullable=False)

    def set_password(self, password):
        """
        Set the password for the user, hashing it before storage.

        Args:
            password (str): The plain-text password to hash and store.
        """
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """
        Check if the provided password matches the stored hashed password.

        Args:
            password (str): The plain-text password to check.

        Returns:
            bool: True if the password matches, False otherwise.
        """
        return check_password_hash(self.password, password)
