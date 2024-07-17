#!/usr/bin/env python3

"""
    imports needed to run the program
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey
from database import Base
from datetime import datetime
from sqlalchemy.orm import relationship


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
    release_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    due_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    description = Column(Text, nullable=False)
    submission_type = Column(String(length=50), nullable=False)
    max_marks = Column(Integer, nullable=False)
    course_id = Column(Integer, ForeignKey('courses.id'), nullable=False)

    course = relationship("Course", back_populates="assignments")

    def __init__(self, name, release_date, due_date, description, submission_type, max_marks, course_id):
        """
            Initialize a new Assignment instance.
        """
        self.name = name
        self.release_date = release_date
        self.due_date = due_date
        self.description = description
        self.submission_type = submission_type
        self.max_marks = max_marks
        self.course_id = course_id
