from .email_utils import send_welcome_email
from .celery import celery_app

@celery_app.task(name="app.tasks.send_welcome_email_task")
def send_welcome_email_task(to_email: str):
    send_welcome_email(to_email)
