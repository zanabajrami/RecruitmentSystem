from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.notification import Notification
from app.schemas.notification import NotificationResponse

router = APIRouter()


@router.get("/user/{user_id}", response_model=List[NotificationResponse])
def get_user_notifications(user_id: int, db: Session = Depends(get_db)):
    """
    Get all system notifications for a specific user.
    """
    notifications = (
        db.query(Notification)
        .filter(Notification.user_id == user_id)
        .order_by(Notification.created_at.desc())
        .all()
    )
    return notifications


@router.patch("/{notification_id}/read", response_model=NotificationResponse)
def mark_notification_as_read(notification_id: int, db: Session = Depends(get_db)):
    """
    Mark a specific notification as read (is_read = True).
    """
    notification = db.query(Notification).filter(Notification.id == notification_id).first()
    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Notification with ID {notification_id} not found."
        )

    notification.is_read = True
    db.commit()
    db.refresh(notification)
    return notification


@router.delete("/{notification_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_notification(notification_id: int, db: Session = Depends(get_db)):
    """
    Delete a specific notification from the database.
    """
    notification = db.query(Notification).filter(Notification.id == notification_id).first()
    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Notification with ID {notification_id} not found."
        )

    db.delete(notification)
    db.commit()
    return None