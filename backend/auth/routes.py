from sqlalchemy.orm import declarative_base
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from auth.utils import get_password_hash, verify_password, create_access_token
from db.session import get_db
from auth.schemas import UserOut, UserCreate, UserLogin
from fastapi.security import OAuth2PasswordRequestForm
from db.models import User
from db.session import get_db
from datetime import timedelta

Base = declarative_base()

# ==============================
# routes.py
# ==============================
auth_router = APIRouter(prefix="/auth", tags=["Auth"])

@auth_router.post("/signup", response_model=UserOut)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = get_password_hash(user.password)
    db_user = User(
        email=user.email,
        full_name=user.full_name,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@auth_router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == form_data.username).first()

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=timedelta(minutes=60)
    )
    return {"access_token": access_token, "token_type": "bearer"}
