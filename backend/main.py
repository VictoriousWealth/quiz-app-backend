from fastapi import FastAPI
from routes.upload import router as upload_router
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from routes.answers import router as answer_router
load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload_router, prefix="/upload", tags=["Upload"])
app.include_router(answer_router, prefix="/answers", tags=["Answers"])


@app.get("/")
def read_root():
    return {"message": "QuizGen FastAPI backend is running!"}


