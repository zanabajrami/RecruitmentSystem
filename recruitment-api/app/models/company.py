from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database.base_model import Base


class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, index=True, nullable=False)
    description = Column(String(1000), nullable=True)
    website = Column(String(255), nullable=True)

    jobs = relationship(
        "Job",
        back_populates="company",
        cascade="all, delete-orphan"
    )