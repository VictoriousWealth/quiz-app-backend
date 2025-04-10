from sqlalchemy.orm import declarative_base
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from auth.utils import get_password_hash, verify_password, create_access_token
from db.session import get_db
from auth.schemas import UserOut, UserCreate, UserLogin

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
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": str(db_user.id)})
    return {"access_token": token, "token_type": "bearer"}
