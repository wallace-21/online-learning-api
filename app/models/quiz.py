from database import Base
from sqlalchemy import Column, Integer, String, DateTime


class Quiz(Base):
    """
        Quiz model for representing quizzes in the database.

        Attributes:
            id (int): The primary key identifier for the quiz.
            name (str): The name of the quiz.
            number_of_questions (int): The number of questions in the quiz.
            marks (int): The total marks for the quiz.
    """
    __tablename__ = "quiz"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(length=25), nullable=False, unique=True)
    number_of_questions = Column(Integer, nullable=False)
    marks = Column(Integer, nullable=False)

    def __init__(self, id, name, number_of_questions, marks):
        """
            Initialize a new Quiz instance.
        """
        self.id = id
        self.name = name
        self.number_of_questions = number_of_questions
        self.marks = marks
