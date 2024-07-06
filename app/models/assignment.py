#!/usr/bin/env python3


from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from database import Base
from datetime import datetime


class Assignment(Base):
    __tablename__ = "assignment"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(length=100), nullable=False, unique=True)
    released_date = Column(DateTime, default=datetime.now)
    due_date = Column(DateTime, nullable=False)
    description = Column(Text, nullable=False)
