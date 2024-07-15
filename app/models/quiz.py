#!/usr/bin/pytho3

"""
    imports that are necessary for the program
"""
from database import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
from sqlalchemy.orm import relationship

class Quiz(Base):
    """
        Quiz model for representing quizzes in the database.

        Attributes:
            id (int): The primary key identifier for the quiz.
            name (str): The name of the quiz.
            number_of_questions (int): The number of questions in the quiz.
            topic (str): What's the quiz about?
            difficulty_level (str): The difficulty level of the quiz.
            duration (int): Allowed time to complete the quiz.
            date_created (datetime): Timestamp when the quiz was created.
            passing_score (int): Minimum score required to pass the quiz.
    """
    __tablename__ = "quiz"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String(length=25), nullable=False, unique=True)
    number_of_questions = Column(Integer, nullable=False)
    topic = Column(String, nullable=False)
    course_id = Column(Integer, ForeignKey('courses.id'), nullable=False)
    difficulty_level = Column(String(length=20), nullable=True)
    duration = Column(Integer, nullable=True)
    date_created = Column(DateTime, default=datetime.utcnow, nullable=False)
    passing_score = Column(Integer, nullable=True)

    course = relationship("Course", back_populates="quizzes")

    def __init__(self, name, number_of_questions, topic, course_id, difficulty_level, duration, passing_score):
        """
            Initialize a new Quiz instance.
        """
        self.name = name
        self.number_of_questions = number_of_questions
        self.topic = topic
        self.course_id = course_id
        self.difficulty_level = difficulty_level
        self.duration = duration
        self.passing_score = passing_score
