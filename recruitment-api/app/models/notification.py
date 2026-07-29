from sqlalchemy import Column, Integer, ForeignKey, Text, Boolean, DateTime, func
from sqlalchemy.orm import relationship
from app.database.base_model import Base


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    title = Column(Text, nullable=False)
    message = Column(Text, nullable=False)
    is_read = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Ndrysho nga backref="notifications" në back_populates="notifications"
    user = relationship("User", back_populates="notifications")