import os
import smtplib
from email.message import EmailMessage

SMTP_HOST = os.getenv("SMTP_HOST", "smtp.sendgrid.net")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER", "apikey")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")  # loaded from environment
FROM_EMAIL = os.getenv("FROM_EMAIL", SMTP_USER or "no-reply@example.com")


def send_welcome_email(to_email: str):
    print(f"[Email] Preparing to send email to {to_email}")
    msg = EmailMessage()
    msg["Subject"] = "Welcome to MyApp 🎉"
    msg["From"] = FROM_EMAIL
    msg["To"] = to_email
    msg.set_content(
        f"Hi,\n\nThanks for registering at MyApp. We're excited to have you.\n\n— The MyApp Team"
    )

    try:
        print(f"[Email] Connecting to SMTP server {SMTP_HOST}:{SMTP_PORT}")
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=30) as server:
            server.ehlo()
            if SMTP_PORT in (587, 25, 2525):
                server.starttls()
                server.ehlo()
            if SMTP_USER and SMTP_PASSWORD:
                print(f"[Email] Logging in as {SMTP_USER}")
                server.login(SMTP_USER, SMTP_PASSWORD)
            server.send_message(msg)
            print("[Email] Email sent successfully!")
    except Exception as e:
        print(f"[Email] Failed to send email: {e}")
