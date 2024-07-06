#!/usr/bin/python3


from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text
from database import Base


class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(length=50), nullable=False, index=True, unique=True)
    price = Column(Integer, nullable=True)
    duration = Column(String(length=25), nullable=False)
    description = Column(Text, nullable=True)
    Certifaction = Column(Boolean, nullable=False)
