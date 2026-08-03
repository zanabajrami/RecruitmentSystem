from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.interview import Interview
from app.models.application import Application
from app.schemas.interview import InterviewCreate, InterviewResponse, InterviewUpdate

router = APIRouter()


@router.post("/", response_model=InterviewResponse, status_code=status.HTTP_201_CREATED)
def schedule_interview(interview_in: InterviewCreate, db: Session = Depends(get_db)):
    """
    Schedule a new interview for a candidate application and notify them.
    """
    from app.models.notification import Notification

    # Verifikojmë nëse ekziston aplikimi
    application = db.query(Application).filter(Application.id == interview_in.application_id).first()
    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Application with ID {interview_in.application_id} not found."
        )

    # Krijojmë intervistën
    db_interview = Interview(**interview_in.model_dump())
    db.add(db_interview)

    # Krijojmë njoftimin për kandidatin
    formatted_date = interview_in.scheduled_at.strftime("%Y-%m-%d %H:%M")
    new_notification = Notification(
        user_id=application.user_id,
        title="Intervistë e Re e Caktuar",
        message=f"Keni një intervistë të caktuar më {formatted_date}. Linku: {interview_in.meeting_link or 'Do të dërgohet së shpejti'}",
        is_read=False
    )
    db.add(new_notification)

    db.commit()
    db.refresh(db_interview)
    return db_interview


@router.get("/application/{application_id}", response_model=List[InterviewResponse])
def get_interviews_for_application(application_id: int, db: Session = Depends(get_db)):
    """
    Get all interviews scheduled for a specific application.
    """
    interviews = db.query(Interview).filter(Interview.application_id == application_id).all()
    return interviews


@router.patch("/{interview_id}", response_model=InterviewResponse)
def update_interview(interview_id: int, interview_in: InterviewUpdate, db: Session = Depends(get_db)):
    """
    Update interview status, meeting link, or rescheduled date.
    """
    interview = db.query(Interview).filter(Interview.id == interview_id).first()
    if not interview:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Interview with ID {interview_id} not found."
        )

    update_data = interview_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(interview, key, value)

    db.commit()
    db.refresh(interview)
    return interview


@router.delete("/{interview_id}", status_code=status.HTTP_204_NO_CONTENT)
def cancel_interview(interview_id: int, db: Session = Depends(get_db)):
    """
    Cancel/delete an interview record.
    """
    interview = db.query(Interview).filter(Interview.id == interview_id).first()
    if not interview:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Interview with ID {interview_id} not found."
        )

    db.delete(interview)
    db.commit()
    return None