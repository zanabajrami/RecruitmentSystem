from sqlalchemy import Column, Integer, ForeignKey, Text, DateTime, String
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.base_model import Base

class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    job_id = Column(Integer, ForeignKey("jobs.id", ondelete="CASCADE"), nullable=False)
    
    # Added string column to track the progress of the application
    status = Column(String(50), default="Pending")  # Pending, Reviewed, Accepted, Rejected
    cover_letter = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Database relationships
    user = relationship("User", back_populates="applications")
    job = relationship("Job", back_populates="applications")