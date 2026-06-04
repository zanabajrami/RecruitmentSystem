from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.database.base_model import Base

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    description = Column(Text, nullable=False)
    
    requirements = Column(Text, nullable=True)
    
    location = Column(String, nullable=False)
    salary = Column(String, nullable=True)  
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)

    # Relationships 
    company = relationship("Company", back_populates="jobs")
    applications = relationship("Application", back_populates="job")