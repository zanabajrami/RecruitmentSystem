from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.application import Application
from app.schemas.application import ApplicationCreate, ApplicationResponse, ApplicationUpdate
from app.services.ai_service import AIService
from app.services.storage_service import storage_service
from app.services.email_service import send_application_email_task

router = APIRouter()


@router.post("/", response_model=ApplicationResponse, status_code=status.HTTP_201_CREATED)
def create_application(app_in: ApplicationCreate, db: Session = Depends(get_db)):
    """
    Create a new job application.
    """
    db_app = Application(**app_in.model_dump())
    db.add(db_app)
    db.commit()
    db.refresh(db_app)
    return db_app


@router.get("/", response_model=List[ApplicationResponse])
def read_applications(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieve a list of job applications with pagination.
    """
    apps = db.query(Application).offset(skip).limit(limit).all()
    return apps


@router.post("/{application_id}/upload-resume", status_code=status.HTTP_200_OK)
async def upload_resume(
    application_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Upload a candidate's resume (PDF/DOCX), update the database record,
    and trigger a background email notification via Celery.
    """
    # Verify application existence
    application = db.query(Application).filter(Application.id == application_id).first()
    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Application with ID {application_id} not found."
        )

    # Save resume file to local storage/S3
    saved_file_path = await storage_service.save_resume(file)

    # Update resume_url field in the database
    application.resume_url = saved_file_path
    db.commit()
    db.refresh(application)

    # Retrieve user and job details for the notification task
    candidate_email = getattr(application.user, "email", "applicant@example.com")
    candidate_name = getattr(application.user, "full_name", "Applicant")
    job_title = getattr(application.job, "title", "Applied Position")

    # Dispatch background task for sending email notification
    send_application_email_task.delay(
        email_to=candidate_email,
        candidate_name=candidate_name,
        job_title=job_title
    )

    return {
        "message": "Resume uploaded successfully and notification email queued.",
        "application_id": application_id,
        "resume_url": saved_file_path
    }


@router.post("/{application_id}/screen", status_code=status.HTTP_200_OK)
def screen_application_with_ai(application_id: int, db: Session = Depends(get_db)):
    """
    Invoke the AI service to screen the candidate's cover letter/resume
    and automatically calculate the matching percentage with job requirements.
    """
    # Importohet brenda funksionit për të parandaluar circular imports
    from app.models.notification import Notification

    application = db.query(Application).filter(Application.id == application_id).first()
    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Application with ID {application_id} not found."
        )
        
    ai_service = AIService(db)
    result = ai_service.screen_application(application_id=application_id)

    # Nxjerrim vlerat nga rezultati i AI
    score = None
    rec = None

    if isinstance(result, dict):
        score = result.get("ai_match_score")
        rec = result.get("recommendation")
    else:
        score = getattr(result, "ai_match_score", None)
        rec = getattr(result, "recommendation", None)

    # Vlerat standarde nëse AI kthen None
    if score is None:
        score = "0.0%"
    if rec is None:
        rec = "LOW MATCH: Background keywords do not line up well with job requirements."

    # Përditësojmë aplikimin
    application.ai_match_score = str(score)
    application.recommendation = str(rec)

    # Krijojmë dhe ruajmë njoftimin në tabelën notifications
    new_notification = Notification(
        user_id=application.user_id,
        title="Rezultati i Screening-ut nga AI",
        message=f"Aplikimi yt u vlerësua: {score}. Recommendation: {rec}",
        is_read=False
    )
    db.add(new_notification)

    db.commit()
    db.refresh(application)

    return {
        "application_id": application.id,
        "candidate_id": application.user_id,
        "ai_match_score": application.ai_match_score,
        "recommendation": application.recommendation
    }


@router.patch("/{application_id}", response_model=ApplicationResponse)
def update_application(
    application_id: int, 
    app_in: ApplicationUpdate, 
    db: Session = Depends(get_db)
):
    """
    Update application metadata, candidate status, or administrative notes.
    """
    application = db.query(Application).filter(Application.id == application_id).first()
    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Application with ID {application_id} not found."
        )
        
    update_data = app_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(application, key, value)
        
    db.commit()
    db.refresh(application)
    return application


@router.delete("/{application_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_application(application_id: int, db: Session = Depends(get_db)):
    """
    Withdraw and permanently delete an application.
    """
    application = db.query(Application).filter(Application.id == application_id).first()
    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Application with ID {application_id} not found."
        )
        
    db.delete(application)
    db.commit()
    return None