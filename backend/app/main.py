import logging
import uuid

from sqlalchemy import and_, delete, insert
from fastapi.security import OAuth2PasswordBearer
from uuid import UUID
from passlib.context import CryptContext
from fastapi import FastAPI, HTTPException, Depends
from typing import Annotated

from app.routes import arrivals, auth, departures, interests, roles, trip_purposes, user
from app import schema, models
from app.database import engine, SessionLocal
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from fastapi.logger import logger
import logging

gunicorn_logger = logging.getLogger("gunicorn.error")
logger.handlers = gunicorn_logger.handlers
if __name__ != "main":
    logger.setLevel(gunicorn_logger.level)
else:
    logger.setLevel(logging.DEBUG)

app = FastAPI(root_path="/api")
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(interests.router)
app.include_router(trip_purposes.router)
app.include_router(departures.router)
app.include_router(arrivals.router)
app.include_router(roles.router)
models.Base.metadata.create_all(bind=engine)

# Assuming app is your FastAPI application instance
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:8000",
        "http://localhost",
        "http://127.0.0.1",
        "http://0.0.0.0",
        "http://192.168.1.129",
    ],  # Add your frontend URL here
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(auth.get_current_user)]

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
