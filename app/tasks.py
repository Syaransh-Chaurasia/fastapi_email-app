import os
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from app.celery_app import celery_app

conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
    MAIL_FROM=os.getenv("MAIL_FROM"),
    MAIL_PORT=int(os.getenv("MAIL_PORT")),
    MAIL_SERVER=os.getenv("MAIL_SERVER"),
    MAIL_STARTTLS=os.getenv("MAIL_STARTTLS") == "True",
    MAIL_SSL_TLS=os.getenv("MAIL_SSL_TLS") == "True",
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
)

@celery_app.task(name="send_welcome_email_task")
def send_welcome_email_task(email: str):
    message = MessageSchema(
        subject="Welcome to FastAPI + Celery Mail",
        recipients=[email],
        body="Thanks for registering at our app!",
        subtype="plain",
    )
    fm = FastMail(conf)
    fm.send_message(message)
