import re
from sqlalchemy.orm import Session
from app.models.application import Application
from app.models.job import Job  # Importojmë direkt modelin Job
from fastapi import HTTPException, status

class AIService:
    def __init__(self, db: Session):
        self.db = db

    def calculate_cv_job_match(self, cover_letter: str, job_description: str) -> float:
        """
        Simple Keyword Matching NLP algorithm.
        Compares job description keywords with candidate's cover letter/CV.
        """
        if not cover_letter or not job_description:
            return 0.0

        job_words = set(re.findall(r'\w+', job_description.lower()))
        cv_words = set(re.findall(r'\w+', cover_letter.lower()))

        # Common words to ignore during matching
        stop_words = {"and", "the", "with", "for", "this", "that", "ne", "me", "per", "nje", "te", "eshte"}
        important_job_keywords = job_words - stop_words

        if not important_job_keywords:
            return 0.0

        matched_keywords = important_job_keywords.intersection(cv_words)
        match_percentage = (len(matched_keywords) / len(important_job_keywords)) * 100
        return round(match_percentage, 2)

    def screen_application(self, application_id: int) -> dict:
        """
        Fetch the application, calculate AI match score, and generate a recommendation.
        """
        # Fetch application directly using the session
        application = self.db.query(Application).filter(Application.id == application_id).first()
        if not application:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Application not found."
            )

        # Fetch the corresponding job listing directly using the session
        job = self.db.query(Job).filter(Job.id == application.job_id).first()
        job_desc = job.description if job and hasattr(job, 'description') else ""
        
        # Calculate matching score
        match_score = self.calculate_cv_job_match(
            cover_letter=application.cover_letter,
            job_description=job_desc
        )

        # Generate recommendation based on score thresholds
        if match_score >= 75.0:
            recommendation = "STRONG MATCH: Highly recommended for an interview."
        elif match_score >= 40.0:
            recommendation = "POTENTIAL MATCH: Needs manual screening."
        else:
            recommendation = "LOW MATCH: Background keywords do not line up well with job requirements."

        return {
            "application_id": application_id,
            "candidate_id": application.user_id,
            "ai_match_score": f"{match_score}%",
            "recommendation": recommendation
        }