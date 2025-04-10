
from sqlalchemy.orm import declarative_base
import uuid
from pydantic import BaseModel, EmailStr

Base = declarative_base()

# ==============================
# schemas.py
# ==============================
class UserCreate(BaseModel):
    email: EmailStr
    full_name: str
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: uuid.UUID
    email: EmailStr
    full_name: str

    class Config:
        orm_mode = True
