from celery import Celery
import os

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

celery_app = Celery(
    "worker",
    broker=REDIS_URL,
    backend=REDIS_URL,
    include=["app.tasks"]  # This should point to the tasks module
)

celery_app.conf.task_routes = {
    "app.tasks.send_welcome_email_task": {"queue": "emails"},
}
