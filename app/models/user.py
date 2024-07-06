from sqlalchemy import Column, String, Integer, Boolean, DateTime
from database import Base
from datetime import datetime

class User(Base):
    __tablename__ = 'users'

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    instructor = Column(Boolean, default=False)
    nationality = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    date_created = Column(DateTime, default=datetime.utcnow)

    def __init__(self, id, name, surname, instructor, nationality, email, password):
        self.id = id
        self.name = name
        self.surname = surname
        self.instructor = instructor
        self.nationality = nationality
        self.email = email
        self.password = password

