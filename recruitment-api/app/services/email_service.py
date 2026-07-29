from app.core.celery_app import celery_app

@celery_app.task(name="send_application_email_task")
def send_application_email_task(email_to: str, candidate_name: str, job_title: str):
    """
    This task is executed by Celery in the background.
    It can be integrated with SendGrid, SMTP, or AWS SES.
    """
    print(f"[EMAIL SERVICE] Sending email to: {email_to}")
    print(f"Hello {candidate_name}, your application for the '{job_title}' position was successfully received!")
    return True