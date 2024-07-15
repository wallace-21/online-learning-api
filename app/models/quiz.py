#!/usr/bin/pytho3

"""
    imports that are necessary for the program
"""
from database import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

class Quiz(Base):
    """
        Quiz model for representing quizzes in the database.

        Attributes:
            id (int): The primary key identifier for the quiz.
            name (str): The name of the quiz.
            number_of_questions (int): The number of questions in the quiz.
            topic (int): What's the quiz about?
    """
    __tablename__ = "quiz"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String(length=25), nullable=False, unique=True)
    number_of_questions = Column(Integer, nullable=False)
    topic = Column(String, nullable=False)
    course_id = Column(Integer, ForeignKey('courses.id'), nullable=False)

    course = relationship("Course", back_populates="quizzes")

    def __init__(self, name, number_of_questions, topic, course_id):
        """
            Initialize a new Quiz instance.
        """
        self.name = name
        self.number_of_questions = number_of_questions
        self.topic = topic
        self.course_id = course_id
