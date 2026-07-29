from sqlalchemy import Column, Integer, ForeignKey, Text, DateTime, String, func
from sqlalchemy.orm import relationship
from app.database.base_model import Base

class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    job_id = Column(Integer, ForeignKey("jobs.id", ondelete="CASCADE"), nullable=False)
    
    # Stores the file path or URL to the candidate's resume/CV
    resume_url = Column(String(255), nullable=True)
    status = Column(String(50), default="Pending", nullable=False)
    cover_letter = Column(Text, nullable=True)
    expected_salary = Column(String(50), nullable=True)
    experience_years = Column(Integer, nullable=True)
    notes = Column(Text, nullable=True)

    # AI screening metrics (KËTO DUAJSHIN TË SHTOHEN)
    ai_match_score = Column(String(50), nullable=True)
    recommendation = Column(Text, nullable=True)

    # Timestamps for audit tracking
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    user = relationship("User", back_populates="applications")
    job = relationship("Job", back_populates="applications")