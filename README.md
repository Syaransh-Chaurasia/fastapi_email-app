# fastapi_email-app

A small FastAPI demo app with:
- HTML register/login pages
- SQLAlchemy-backed users table
- Celery task queue for welcome emails
- SMTP-based email sending in the worker

## Features

- `GET /` home page
- `GET /register` and `POST /register`
- `GET /login` and `POST /login`
- Asynchronous welcome-email task (`send_welcome_email_task`)

## Requirements

- Python 3.10+
- Redis (for Celery broker/result backend)

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Update `.env` values before using real email sending.

## Environment variables

Used directly by the running app/worker:

- `DATABASE_URL` (default: `sqlite:///./test.db`)
- `REDIS_URL` (preferred) or `CELERY_BROKER_URL` (fallback)
- `SMTP_HOST`
- `SMTP_PORT` (default `587`)
- `SMTP_USER`
- `SMTP_PASSWORD`
- `SMTP_FROM_EMAIL` (default `noreply@example.com`)
- `SMTP_USE_TLS` (`True`/`False`, default `True`)

Used by auth utility module (`app/auth.py`):

- `SECRET_KEY`
- `ALGORITHM` (default `HS256`)
- `ACCESS_TOKEN_EXPIRE_MINUTES` (default `1440`)

## Run locally

Start API:

```bash
uvicorn app.main:app --reload
```

Start Celery worker (new terminal):

```bash
celery -A celery_worker.celery_app worker --loglevel=info
```

## Database notes

- For SQLite, the app will auto-create the `users` table at startup.
- If `DATABASE_URL` is left unset, `test.db` is created locally.

## Smoke test

Run a lightweight local smoke test that verifies the app imports and routes are registered:

```bash
python -m unittest discover -s tests -v
```

This test does not require Redis or SMTP credentials.
