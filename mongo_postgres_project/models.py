from pydantic import BaseModel, EmailStr
from typing import Optional
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    full_name = Column(String, nullable=True)

class UserBase(BaseModel):
    email: EmailStr
    password: str
    phone: str
    first_name: str
    full_name: Optional[str]

class UserCreate(UserBase):
    pass
