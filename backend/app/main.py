from fastapi import FastAPI

from app.chat.router import chat_router
from app.user.router import user_router
from app.auth.router import auth_router
from app.routes import (
    interests,
    trip_purposes,
    departures,
    arrivals,
)
from app import models
from app.database import engine
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(root_path="/api")

app.include_router(auth_router)
app.include_router(chat_router)
app.include_router(user_router)
app.include_router(interests.router)
app.include_router(trip_purposes.router)
app.include_router(departures.router)
app.include_router(arrivals.router)

models.Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost",
        "http://192.168.1.128",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
