import logging
from fastapi import FastAPI

from app.chat.router import chat_router
from app.user.router import user_router
from app.routes import (
    auth,
    interests,
    trip_purposes,
    departures,
    arrivals,
)
from app import models
from app.database import engine
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
app.include_router(chat_router)
app.include_router(user_router)
app.include_router(interests.router)
app.include_router(trip_purposes.router)
app.include_router(departures.router)
app.include_router(arrivals.router)
# app.include_router(roles.router)

models.Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:8000",
        "http://localhost",
        "http://127.0.0.1",
        "http://0.0.0.0",
        "http://192.168.1.129",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
