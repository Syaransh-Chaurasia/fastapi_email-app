# app/main.py
import os
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, Request, Form, Depends, status
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from .db import SessionLocal, engine, Base
from . import models
from app.tasks import send_welcome_email_task  # Celery task import

# Create DB tables (run on app startup)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="fastapi-celery-mail")

# Templates and static setup
templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), "templates"))
static_dir = os.path.join(os.path.dirname(__file__), "static")
if not os.path.isdir(static_dir):
    os.makedirs(static_dir, exist_ok=True)
app.mount("/static", StaticFiles(directory=static_dir), name="static")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_db():
    """
    DB dependency that yields an SQLAlchemy Session.
    Use with `Depends(get_db)` in endpoints.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def index(request: Request):
    return templates.TemplateResponse("base.html", {"request": request})

@app.get("/register")
def register_get(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.post("/register")
def register_post(
        request: Request,
        email: str = Form(...),
        password: str = Form(...),
        db: Session = Depends(get_db),
):
    # Check if user already exists
    existing = db.query(models.User).filter(models.User.email == email).first()
    if existing:
        return templates.TemplateResponse(
            "register.html", {"request": request, "error": "Email already registered"}
        )

    # Hash password and create user
    hashed = pwd_context.hash(password)
    user = models.User(email=email, hashed_password=hashed)
    db.add(user)
    db.commit()
    db.refresh(user)

    # Queue welcome email with Celery (async task)
    try:
        send_welcome_email_task.delay(user.email)
    except Exception:
        # If Celery/Redis unreachable, succeed registration but show warning
        return templates.TemplateResponse(
            "register.html",
            {
                "request": request,
                "error": "Registration succeeded but failed to queue welcome email. Check Celery/Redis.",
            },
            status_code=status.HTTP_201_CREATED,
        )

    return RedirectResponse(url="/login?msg=registered", status_code=status.HTTP_303_SEE_OTHER)

@app.get("/login")
def login_get(request: Request, msg: str | None = None):
    ctx = {"request": request}
    if msg == "registered":
        ctx["success"] = "Account created. A welcome email was sent (check spam)."
    return templates.TemplateResponse("login.html", ctx)

@app.post("/login")
def login_post(
        request: Request,
        email: str = Form(...),
        password: str = Form(...),
        db: Session = Depends(get_db),
):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user or not pwd_context.verify(password, user.hashed_password):
        return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid credentials"})

    # Normally, you'd create a session or JWT here.
    return templates.TemplateResponse("login.html", {"request": request, "success": f"Welcome back, {email}!"})
