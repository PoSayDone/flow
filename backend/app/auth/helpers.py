from datetime import UTC, datetime, timedelta
from urllib import parse

from fastapi import HTTPException, status
from fastapi.security.utils import get_authorization_scheme_param
from jose import JWTError, jwt

from app.models import Users

SECRET_KEY = "4bad42439cea6743a225bc13fcaacf0bbf637edbb197d96611f2b40c36ce724c"
REFRESH_SECRET_KEY = "ee4073ce6711053c8006cf225ff9af00a0ae3350340d29cb580356cddec3097fa0645c0ff6cd12724e2fc544551c47598d39638df38abf045e3ebeae97b853e0"
ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 10
REFRESH_TOKEN_EXPIRE_DAYS = 90


def create_access_token(user: Users) -> tuple[datetime, str]:
    encode: dict = {"sub": user.mail, "mail": user.mail, "id": str(user.id)}
    expires = datetime.now(UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    encode.update({"exp": expires})
    return expires, jwt.encode(encode, key=SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token(user: Users) -> tuple[datetime, str]:
    encode: dict = {"sub": user.mail, "id": str(user.id)}
    expires = datetime.now(UTC) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    encode.update({"exp": expires})
    return expires, jwt.encode(encode, key=REFRESH_SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user"
        )


def decode_refresh_token(token):
    try:
        return jwt.decode(token, REFRESH_SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user"
        )
