# celery_worker.py
# Simple module to allow the Celery CLI to discover the app: `celery -A celery_worker.celery_app worker ...`
from app.tasks import celery_app  # noqa: F401
