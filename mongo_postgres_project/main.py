from fastapi import FastAPI, Depends, HTTPException, status, File, UploadFile, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database import engine, Base, get_db
from models import User, UserCreate
from passlib.context import CryptContext
from pymongo import MongoClient
import gridfs
from typing import Optional
from pydantic import BaseModel as PydanticBaseModel
import bson
import base64


app = FastAPI()

templates = Jinja2Templates(directory="templates")

Base.metadata.create_all(bind=engine)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

MONGO_URL = "mongodb+srv://Hariomsimform123:w6dLtUqi7Bim9Jxl@cluster0.ealz30c.mongodb.net/"
MONGO_DB_NAME = "user_profile"

client = MongoClient(MONGO_URL)
mongo_db = client[MONGO_DB_NAME]
fs = gridfs.GridFS(mongo_db)

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
    
    # Fetch profile picture from MongoDB
    user_profile = mongo_db.profile_pictures.find_one({"email": email})
    profile_picture = None
    if user_profile:
        profile_picture_id = user_profile["picture_id"]
        profile_picture = fs.get(profile_picture_id).read()
        profile_picture_base64 = base64.b64encode(profile_picture).decode('utf-8')
    
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
    existing_user = db.query(User).filter(User.email == email).first()
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
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    if profile_picture:
        file_content = profile_picture.file.read()
        save_profile_picture(email, file_content)
    
    return {"message": "User registered successfully"}

def save_profile_picture(email: str, file_content: bytes):
    user_profile = mongo_db.profile_pictures.find_one({"email": email})
    if user_profile:
        fs.delete(user_profile["picture_id"])
        mongo_db.profile_pictures.delete_one({"email": email})
    
    picture_id = fs.put(file_content)
    mongo_db.profile_pictures.insert_one({"email": email, "picture_id": picture_id})
