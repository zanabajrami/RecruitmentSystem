from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database.session import get_db
from app.models.application import Application
from app.schemas.application import ApplicationCreate, ApplicationResponse, ApplicationUpdate
from app.services.ai_service import AIService

router = APIRouter()

@router.post("/", response_model=ApplicationResponse)
def create_application(app_in: ApplicationCreate, db: Session = Depends(get_db)):
    db_app = Application(**app_in.model_dump())
    db.add(db_app)
    db.commit()
    db.refresh(db_app)
    return db_app

@router.get("/", response_model=List[ApplicationResponse])
def read_applications(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    apps = db.query(Application).offset(skip).limit(limit).all()
    return apps

@router.post("/{application_id}/screen", status_code=status.HTTP_200_OK)
def screen_application_with_ai(application_id: int, db: Session = Depends(get_db)):
    """
    Invoke the AI service to screen the candidate's cover letter/resume
    and automatically calculate the matching percentage with job requirements.
    """
    # Check if the application exists in the database
    app_exists = db.query(Application).filter(Application.id == application_id).first()
    if not app_exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Application with ID {application_id} not found."
        )
        
    # Initialize the AI service and execute the screening process
    ai_service = AIService(db)
    return ai_service.screen_application(application_id=application_id)

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