import logging
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

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
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):

    exc_str = f"{exc}".replace("\n", " ").replace("   ", " ")
    # or logger.error(f'{exc}')
    logger.error(request, exc_str)
    content = {"status_code": 10422, "message": exc_str, "data": None}
    return JSONResponse(
        content=content, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
    )
