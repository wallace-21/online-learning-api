from database import Base
from sqlalchemy import Column, Integer, String, DateTime


class Quiz(Base):
    __tablename__ = "quiz"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(length=25), nullable=False, unique=True)
    number_of_questions = Column(Integer, nullable=False)
    marks = Column(Integer, nullable=False)
