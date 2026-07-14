import re
from sqlalchemy.orm import Session
from app.models.application import Application
from app.models.job import Job
from fastapi import HTTPException, status

class AIService:
    """
    Business logic layer for screening applications using a lightweight
    Natural Language Processing (NLP) heuristic algorithm.
    """
    def __init__(self, db: Session):
        self.db = db

    def calculate_cv_job_match(self, cover_letter: str, job_description: str) -> float:
        """
        Calculates compatibility between candidate cover letters and job listings
        by computing intersection percentages on key semantic terms.
        """
        if not cover_letter or not job_description:
            return 0.0

        # Tokenize job and cover letter descriptions into words, normalized to lowercase
        job_words = re.findall(r'\w+', job_description.lower())
        cv_words = re.findall(r'\w+', cover_letter.lower())

        # Filter out short grammatical particles, connectors, and short words (length < 4)
        # This automatically excludes words like: me, ne, te, per, and, the, for, with
        important_job_keywords = {word for word in job_words if len(word) >= 4}
        important_cv_keywords = {word for word in cv_words if len(word) >= 4}

        if not important_job_keywords:
            return 0.0

        # Calculate keyword match percentage based only on substantial words
        matched_keywords = important_job_keywords.intersection(important_cv_keywords)
        match_percentage = (len(matched_keywords) / len(important_job_keywords)) * 100
        return round(match_percentage, 2)

    def screen_application(self, application_id: int) -> dict:
        """
        Processes candidate applications, cross-references with target jobs,
        evaluates keyword compatibility, and generates a structured fit recommendation.
        """
        # Fetch application record directly from the database session
        application = self.db.query(Application).filter(Application.id == application_id).first()
        if not application:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Application not found."
            )

        # Retrieve the related job listing
        job = self.db.query(Job).filter(Job.id == application.job_id).first()
        job_desc = job.description if job and hasattr(job, 'description') else ""
        
        # Determine the NLP matching score
        match_score = self.calculate_cv_job_match(
            cover_letter=application.cover_letter,
            job_description=job_desc
        )

        # Classify recommendation levels based on target matching thresholds
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