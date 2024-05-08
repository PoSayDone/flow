from datetime import UTC, datetime, timedelta

from fastapi import HTTPException, status
from jose import JWTError, jwt

from app.core.config import settings
from app.models import Users

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 10
REFRESH_TOKEN_EXPIRE_DAYS = 90


def create_access_token(user: Users) -> tuple[datetime, str]:
    encode: dict = {"sub": user.mail, "mail": user.mail, "id": str(user.id)}
    expires = datetime.now(UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    encode.update({"exp": expires})
    return expires, jwt.encode(
        encode, key=settings.access_secret_key, algorithm=ALGORITHM
    )


def create_refresh_token(user: Users) -> tuple[datetime, str]:
    encode: dict = {"sub": user.mail, "id": str(user.id)}
    expires = datetime.now(UTC) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    encode.update({"exp": expires})
    return expires, jwt.encode(
        encode, key=settings.refresh_secret_key, algorithm=ALGORITHM
    )


def decode_access_token(token):
    try:
        return jwt.decode(token, settings.access_secret_key, algorithms=ALGORITHM)
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user"
        )


def decode_refresh_token(token):
    try:
        return jwt.decode(token, settings.refresh_secret_key, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user"
        )
