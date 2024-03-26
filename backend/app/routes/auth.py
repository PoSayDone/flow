from datetime import datetime, timedelta
from typing import Annotated
from urllib import parse
from uuid import UUID
from fastapi.security.utils import get_authorization_scheme_param
from jose import jwt, JWTError
from fastapi import APIRouter, Cookie, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from passlib.context import CryptContext
from pydantic import EmailStr
from sqlalchemy.orm import Session
from app import models
from app.database import SessionLocal

from app.utils import OAuth2PasswordBearerWithCookie

from app.models import Users
from app.schema import TokenBase, UserCreateRequest


SECRET_KEY = "4bad42439cea6743a225bc13fcaacf0bbf637edbb197d96611f2b40c36ce724c"
REFRESH_SECRET_KEY = "ee4073ce6711053c8006cf225ff9af00a0ae3350340d29cb580356cddec3097fa0645c0ff6cd12724e2fc544551c47598d39638df38abf045e3ebeae97b853e0"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 10
REFRESH_TOKEN_EXPIRE_DAYS = 90

router = APIRouter(prefix="/auth", tags=["auth"])

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="auth/token")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


@router.post("/refresh", response_model=TokenBase)
async def refresh_token_regenerate(
    db: db_dependency,
    refresh_token_cookie: str = Cookie(alias="refresh_token"),
):
    refresh_token: str = parse.unquote(refresh_token_cookie)
    _, refresh_token = get_authorization_scheme_param(refresh_token)
    payload = jwt.decode(refresh_token, REFRESH_SECRET_KEY, algorithms=[ALGORITHM])
    user_id = UUID(payload.get("id"))
    mail = str(payload.get("sub"))

    refresh_token = (
        db.query(models.RefreshTokens)
        .filter_by(user_id=user_id, refresh_token=refresh_token)
        .first()
    )
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    # Revoke previous refresh tokens for this user (optional security measure)
    db.query(models.RefreshTokens).filter_by(user_id=user_id).delete()

    # Create new access token and refresh token
    new_access_token = create_access_token(
        mail, user_id, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    new_refresh_token = create_refresh_token(
        mail, user_id, timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    )

    # Store new refresh token in database
    refresh_token_db = models.RefreshTokens(
        refresh_token=new_refresh_token,
        user_id=user_id,
        expires_at=datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS),
    )
    db.add(refresh_token_db)
    db.commit()

    return {
        "access_token": new_access_token,
        "refresh_token": new_refresh_token,
        "token_type": ALGORITHM,
    }


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, user_create_request: UserCreateRequest):
    user_create_model = Users(
        id=user_create_request.id,
        name=user_create_request.name,
        mail=user_create_request.mail,
        password_hash=bcrypt_context.hash(user_create_request.password),
    )
    db.add(user_create_model)
    db.commit()


@router.post("/token", response_model=TokenBase)
async def login_for_access_token(
    response: Response,
    db: db_dependency,
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    authenticated_user = authneticate_user(form_data.username, form_data.password, db)
    if not authenticated_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user"
        )

    access_token = create_access_token(
        authenticated_user.mail,
        authenticated_user.id,
        timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    refresh_token = create_refresh_token(
        authenticated_user.mail,
        authenticated_user.id,
        timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS),
    )

    existing_refresh = db.query(models.RefreshTokens).get(authenticated_user.id)

    if existing_refresh:
        db.delete(existing_refresh)

    new_refresh_token = models.RefreshTokens(
        refresh_token=refresh_token,
        user_id=authenticated_user.id,
        expires_at=datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS),
    )
    db.add(new_refresh_token)
    db.commit()

    response.set_cookie(
        key="access_token_zhopa",
        value=f"Bearer {access_token}",
        httponly=True,
        path="/",
    )
    response.set_cookie(
        key="refresh_token", value=f"Bearer {refresh_token}", httponly=True, path="/"
    )
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


def authneticate_user(mail: EmailStr, password: str, db: db_dependency):
    user = db.query(Users).filter(Users.mail == mail).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.password_hash):
        return False
    return user


def create_access_token(mail: EmailStr, user_id: UUID, expires_date: timedelta):
    encode: dict = {"sub": mail, "id": user_id.__str__()}
    expires = datetime.utcnow() + expires_date
    encode.update({"exp": expires})
    return jwt.encode(encode, key=SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token(mail: EmailStr, user_id: UUID, expires_date: timedelta):
    encode: dict = {"sub": mail, "id": user_id.__str__()}
    expires = datetime.utcnow() + expires_date
    encode.update({"exp": expires})
    return jwt.encode(encode, key=REFRESH_SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        mail: str = str(payload.get("sub"))
        id: UUID = UUID(payload.get("id"))
        if mail is None or id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate user",
            )
        return {"mail": mail, "id": id.__str__()}
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user"
        )
