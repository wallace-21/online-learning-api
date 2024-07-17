#!/bin/python3

"""
    imports that are necessary for the program
"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
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
            created_date (datetime): The date when the lecture was created.
            duration (int): How long will the lecture tak?
            course_id (int): course associated with this lecture
    """

    __tablename__ = "lecture"

    id = Column(Integer, nullable=False, primary_key=True)
    name = Column(String(length=50), nullable=False, unique=True)
    date_and_time = Column(DateTime, nullable=False)
    mentors = Column(String(length=50), nullable=False)
    created_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    duration = Column(Integer, nullable=False)
    course_id = Column(Integer, ForeignKey('courses.id'), nullable=False)

    course = relationship("Course", back_populates="lectures")

    def __init__(self, name, date_and_time, mentors, duration, course_id):
        """
            Initialize a new Lecture instance
        """
        self.name = name
        self.date_and_time = date_and_time
        self.mentors = mentors
        self.duration = duration
        self.course_id = course_id
