from sqlalchemy import (
    Column, Integer, String, Float, Boolean, Text, DateTime,
    ForeignKey, Enum
)
from sqlalchemy.orm import relationship
from datetime import datetime
from app.utils.db import Base
import uuid



class EnrollmentStatus(enum.Enum):
    NOT_STARTED = "not-started"
    IN_PROGRESS = "in-progress"
    COMPLETED = "completed"
    DROPPED = "dropped"


class Enrollment(Base):
    __tablename__ = 'enrollments'
    id = Column(String(36), primary_key=True, default=lambda: f"enrollment-{uuid.uuid4().hex[:8]}")
    user_id = Column(String(36), ForeignKey('users.id'), nullable=False)
    course_id = Column(String(36), ForeignKey('courses.id'), nullable=False)
    course_name = Column(String(255))
    enrollment_date = Column(DateTime, default=datetime.utcnow)
    status = Column(Enum(EnrollmentStatus), default=EnrollmentStatus.NOT_STARTED)
    expiry_date = Column(DateTime)
    progress = Column(Integer, default=0)  # percentage
    last_access_date = Column(DateTime)
    completion_date = Column(DateTime)
    certificate_issued = Column(Boolean, default=False)
    certificate_url = Column(String(255))
    favorite = Column(Boolean, default=False)

    user = relationship("User", back_populates="enrollments")
    def __repr__(self):
        return f"<Enrollment {self.id}>"
