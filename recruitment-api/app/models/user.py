from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database.base_model import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(50), default="candidate")

    applications = relationship(
        "Application",
        back_populates="user",
        cascade="all, delete-orphan"
    )