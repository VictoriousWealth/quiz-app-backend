from db.models import Base
from db.session import engine

from fastapi import FastAPI
from routes.upload import router as upload_router
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from routes.answers import router as answer_router
from db.session import get_db
from sqlalchemy.orm import Session
from routes.upload_db import router as upload_db_router
from fastapi import Depends
from sqlalchemy.orm import Session
from auth.routes import auth_router

load_dotenv()

Base.metadata.create_all(bind=engine)  # Temporary until you use Alembic

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(upload_router, prefix="/upload", tags=["Upload"])
app.include_router(answer_router, prefix="/answers", tags=["Answers"])
app.include_router(upload_db_router, prefix="/upload-db", tags=["Upload & Store"])


@app.get("/")
def read_root(db: Session = Depends(get_db)):
    return {"message": "QuizGen FastAPI backend is running!"}


