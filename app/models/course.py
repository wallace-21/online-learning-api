#!/usr/bin/python3

"""
    imports necessary for the program
"""
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text
from database import Base
from sqlalchemy.orm import relationship


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

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String(length=50), nullable=False, index=True, unique=True)
    price = Column(Integer, nullable=True)
    duration = Column(String(length=25), nullable=False, default="self-paced")
    description = Column(Text, nullable=True)
    certification = Column(Boolean, nullable=False, default=False)
    language = Column(String(length=20), nullable=False)
    tags = Column(String(length=100), nullable=True)
    max_students = Column(Integer, nullable=False)
    # number_of_assignment = Column(Integer, nullable=False)
    # number_of_lectures = Column(Integer, nullable=False)
    # number_of_quizzes = Column(Integer, nullable=False)

    quizzes = relationship("Quiz", back_populates="course")
    assignments = relationship("Assignment", back_populates="course")

    def __init__(self, name, price, duration, description, certification, language, tags, max_students):
        """
            Initialize a new Course instance
        """
        self.name = name
        self.price = price
        self.duration = duration
        self.description = description
        self.certification = certification
        self.language = language
        self.tags = tags
        self.max_students = max_students
