from sqlalchemy import Column, Integer, String, DateTime
from database import Base
from datetime import datetime


class Lecture(Base):
    __tablename__ = "lecture"

    id = Column(Integer, nullable=False, primary_key=True)
    name = Column(String(length=50), nullable=False, unique=True)
    date_and_time = Column(DateTime, nullable=False)
    mentors = Column(String(length=50), nullable=False)
