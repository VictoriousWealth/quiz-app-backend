from sqlalchemy import (
    Column, String, Integer, ForeignKey, Boolean,
    DateTime, Text, JSON
)
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.sql import func
import uuid
from sqlalchemy.dialects.postgresql import UUID


Base = declarative_base()

def generate_uuid():
    return str(uuid.uuid4())

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=generate_uuid)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, nullable=True)
    full_name = Column(String, nullable=True)  # Optional
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    uploads = relationship("UploadedFile", back_populates="user")
    attempts = relationship("QuizAttempt", back_populates="user")



class UploadedFile(Base):
    __tablename__ = "uploaded_files"

    id = Column(UUID(as_uuid=True), primary_key=True, default=generate_uuid)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    filename = Column(String, nullable=False)
    original_name = Column(String, nullable=True)
    file_type = Column(String)
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="uploads")
    quizzes = relationship("Quiz", back_populates="file")


class Quiz(Base):
    __tablename__ = "quizzes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=generate_uuid)
    file_id = Column(UUID(as_uuid=True), ForeignKey("uploaded_files.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    file = relationship("UploadedFile", back_populates="quizzes")
    questions = relationship("Question", back_populates="quiz")
    attempts = relationship("QuizAttempt", back_populates="quiz")


class Question(Base):
    __tablename__ = "questions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=generate_uuid)
    quiz_id = Column(String, ForeignKey("quizzes.id"))
    text = Column(Text)
    options = Column(JSON)  # Expects list of strings
    correct_answer = Column(String)
    explanation = Column(Text)

    quiz = relationship("Quiz", back_populates="questions")
    answers = relationship("UserAnswer", back_populates="question")


class QuizAttempt(Base):
    __tablename__ = "quiz_attempts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=generate_uuid)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    quiz_id = Column(UUID(as_uuid=True), ForeignKey("quizzes.id"))
    score = Column(Integer)
    submitted_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="attempts")
    quiz = relationship("Quiz", back_populates="attempts")
    answers = relationship("UserAnswer", back_populates="attempt")


class UserAnswer(Base):
    __tablename__ = "user_answers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=generate_uuid)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    question_id = Column(UUID(as_uuid=True), ForeignKey("questions.id"))
    attempt_id = Column(UUID(as_uuid=True), ForeignKey("quiz_attempts.id"))
    answer = Column(String)
    is_correct = Column(Boolean)
    submitted_at = Column(DateTime(timezone=True), server_default=func.now())

    question = relationship("Question", back_populates="answers")
    attempt = relationship("QuizAttempt", back_populates="answers")
