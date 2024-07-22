from fastapi import FastAPI, Depends, HTTPException, status, File, UploadFile, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database import engine, Base, get_db
from models import User
from passlib.context import CryptContext
from typing import Optional
from pydantic import BaseModel as PydanticBaseModel
import base64

app = FastAPI()

templates = Jinja2Templates(directory="templates")

Base.metadata.create_all(bind=engine)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

class UserLogin(PydanticBaseModel):
    email: str
    password: str

class UserResponse(PydanticBaseModel):
    email: str
    full_name: Optional[str]
    first_name: str
    phone: str
    profile_picture: Optional[str]

# Helper function to get user by email
def get_user(db, email: str):
    return db.query(User).filter(User.email == email).first()

@app.get("/register/", response_class=HTMLResponse)
def register_form(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.get("/login", response_class=HTMLResponse)
def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login", response_model=UserResponse)
def login(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    # Fetch user from database
    user = get_user(db, email)

    if user is None:
        raise HTTPException(status_code=400, detail="Invalid email or password")
    
    # Verify password
    if not verify_password(password, user.password):
        raise HTTPException(status_code=400, detail="Invalid email or password")
    
    # Convert profile picture to base64
    profile_picture_base64 = None
    if user.profile_picture:
        profile_picture_base64 = base64.b64encode(user.profile_picture).decode('utf-8')
    
    # Return user details
    return templates.TemplateResponse("user_details.html", {
        "request": request,
        "email": user.email,
        "full_name": user.full_name,
        "first_name": user.first_name,
        "phone": user.phone,
        "profile_picture": profile_picture_base64
    })

@app.post("/register/", status_code=status.HTTP_201_CREATED)
def register_user(
    email: str = Form(...),
    password: str = Form(...),
    phone: str = Form(...),
    first_name: str = Form(...),
    full_name: str = Form(None),
    profile_picture: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    # Check if email already exists
    existing_user = get_user(db, email)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    
    # Create new user
    hashed_password = hash_password(password)
    new_user = User(
        email=email,
        password=hashed_password,
        phone=phone,
        first_name=first_name,
        full_name=full_name
    )
    
    if profile_picture:
        new_user.profile_picture = profile_picture.file.read()
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return {"message": "User registered successfully"}
