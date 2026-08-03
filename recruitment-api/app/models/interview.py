from sqlalchemy import Column, Integer, ForeignKey, String, DateTime, Enum, Text, func
from sqlalchemy.orm import relationship
import enum

from app.database.base_model import Base


class InterviewStatus(str, enum.Enum):
    SCHEDULED = "SCHEDULED"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


class Interview(Base):
    __tablename__ = "interviews"

    id = Column(Integer, primary_key=True, index=True)
    application_id = Column(Integer, ForeignKey("applications.id", ondelete="CASCADE"), nullable=False)
    scheduled_at = Column(DateTime(timezone=True), nullable=False)
    meeting_link = Column(String(255), nullable=True)
    notes = Column(Text, nullable=True)
    status = Column(String(50), default=InterviewStatus.SCHEDULED, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Marrëdhëniet
    application = relationship("Application", backref="interviews")