# app/email_utils.py
import os
from dotenv import load_dotenv
load_dotenv()
import smtplib
from email.message import EmailMessage

SMTP_HOST = os.getenv("SMTP_HOST", "")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
SMTP_FROM_EMAIL = os.getenv("SMTP_FROM_EMAIL", "noreply@example.com")
SMTP_USE_TLS = os.getenv("SMTP_USE_TLS", "True").lower() in ("1", "true", "yes")

def send_welcome_email(to_email: str, name: str | None = None) -> None:
    """
    Send a simple welcome email synchronously (this function will be called inside Celery worker).
    """
    subject = "Welcome!"
    body = f"Hi {name or ''},\n\nThanks for registering. Welcome aboard!\n\n— The Team"

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = SMTP_FROM_EMAIL
    msg["To"] = to_email
    msg.set_content(body)

    if SMTP_USE_TLS:
        server = smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=10)
        server.starttls()
    else:
        server = smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, timeout=10)

    # if user/pass provided, login; else skip (some SMTP relays don't require)
    if SMTP_USER and SMTP_PASSWORD:
        server.login(SMTP_USER, SMTP_PASSWORD)

    server.send_message(msg)
    server.quit()
