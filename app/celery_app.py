from celery import Celery
import os
from dotenv import load_dotenv

load_dotenv()

# Get Redis URL from environment or fallback (update your env on Render)
redis_url = os.getenv(
    "REDIS_URL",
    "redis://:<password>@redis-17850.c90.us-east-1-3.ec2.redns.redis-cloud.com:17850/0"
)

celery_app = Celery(
    "worker",
    broker=redis_url,
    backend=redis_url
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)
