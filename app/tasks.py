from app.celery_app import celery_app
from app.email_utils import send_welcome_email

@celery_app.task(name="send_welcome_email_task")
def send_welcome_email_task(email: str, name: str | None = None):
    """
    Celery task to send welcome email asynchronously via smtplib.
    """
    send_welcome_email(to_email=email, name=name)
