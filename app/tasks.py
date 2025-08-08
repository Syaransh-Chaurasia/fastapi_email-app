from .celery_worker import celery_app
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from dotenv import load_dotenv

load_dotenv()

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
EMAIL_FROM = os.getenv("EMAIL_FROM")

@celery_app.task
def send_email_task(to_email: str, subject: str, body: str):
    message = Mail(
        from_email=EMAIL_FROM,
        to_emails=to_email,
        subject=subject,
        html_content=body
    )
    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        sg.send(message)
        return {"status": "Email sent successfully"}
    except Exception as e:
        return {"status": "failed", "error": str(e)}

@celery_app.task
def send_welcome_email_task(to_email: str):
    subject = "Welcome to Our Service!"
    body = """
    <h1>Welcome!</h1>
    <p>Thank you for registering. We're excited to have you with us.</p>
    """
    # Call the generic send_email_task synchronously here (within Celery task)
    return send_email_task(to_email, subject, body)
