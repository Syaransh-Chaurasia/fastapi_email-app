from dotenv import load_dotenv
load_dotenv()

import os
from fastapi import FastAPI, Request, Form, BackgroundTasks, Depends, status
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from .database import SessionLocal, engine, Base
from . import models
from .email_utils import send_welcome_email

Base.metadata.create_all(bind=engine)

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_db():
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
        background_tasks: BackgroundTasks,
        email: str = Form(...),
        password: str = Form(...),
        db: Session = Depends(get_db),
):
    existing = db.query(models.User).filter(models.User.email == email).first()
    if existing:
        return templates.TemplateResponse(
            "register.html", {"request": request, "error": "Email already registered"}
        )

    hashed = pwd_context.hash(password)
    user = models.User(email=email, hashed_password=hashed)
    db.add(user)
    db.commit()
    db.refresh(user)

    background_tasks.add_task(send_welcome_email, user.email)

    return RedirectResponse(url="/login?msg=registered", status_code=status.HTTP_303_SEE_OTHER)

@app.get("/login")
def login_get(request: Request, msg: str = None):
    ctx = {"request": request}
    if msg == "registered":
        ctx["success"] = "Account created. A welcome email was sent (check spam)."
    return templates.TemplateResponse("login.html", ctx)

@app.post("/login")
def login_post(request: Request, email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user or not pwd_context.verify(password, user.hashed_password):
        return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid credentials"})
    return templates.TemplateResponse("login.html", {"request": request, "success": f"Welcome back, {email}!"})
