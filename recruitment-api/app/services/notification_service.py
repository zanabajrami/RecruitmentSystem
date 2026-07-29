from sqlalchemy.orm import Session
from app.models.notification import Notification

class NotificationService:
    def __init__(self, db: Session):
        self.db = db

    def create_notification(self, user_id: int, title: str, message: str) -> Notification:
        notif = Notification(
            user_id=user_id,
            title=title,
            message=message
        )
        self.db.add(notif)
        self.db.commit()
        self.db.refresh(notif)
        return notif

    def get_user_notifications(self, user_id: int):
        return self.db.query(Notification).filter(Notification.user_id == user_id).all()