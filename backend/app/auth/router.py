from datetime import UTC, datetime
from uuid import UUID
import uuid
from fastapi import APIRouter, Cookie, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from app import models

from app.auth.helpers import (
    create_access_token,
    create_refresh_token,
    decode_refresh_token,
)
from app.auth.services import (
    authneticate_user,
    bcrypt_context,
    get_user_by_id,
    get_user_by_mail,
)
from app.models import Users
from app.schema import TokenBase, UserCreateRequest
from app.dependencies import db_dependency


auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.get("/check_email/{mail}")
async def check_email(db: db_dependency, mail: str):
    exists = db.query(models.Users).filter(models.Users.mail == mail).first()
    if exists:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists",
        )
    return {"ok"}


@auth_router.post("/signup", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, user_create_request: UserCreateRequest):

    exists = get_user_by_mail(user_create_request.mail, db)
    if exists:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists",
        )
    user_create_model = Users(
        id=uuid.uuid4(),
        name=user_create_request.name,
        mail=user_create_request.mail,
        birthdate=user_create_request.birthdate,
        sex=user_create_request.sex,
        password_hash=bcrypt_context.hash(user_create_request.password),
        registration_date=datetime.now(UTC),
    )
    db.add(user_create_model)
    db.commit()
    return {"ok"}


@auth_router.post("/signin")
async def login_for_access_token(
    response: Response,
    db: db_dependency,
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    user = authneticate_user(form_data.username, form_data.password, db)

    access_token_expires, access_token = create_access_token(user)
    refresh_token_expires, refresh_token = create_refresh_token(user)

    existing_refresh = db.query(models.RefreshTokens).get(user.id)

    if existing_refresh:
        db.delete(existing_refresh)

    new_refresh_token = models.RefreshTokens(
        refresh_token=refresh_token,
        user_id=user.id,
    )
    db.add(new_refresh_token)
    db.commit()

    response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        httponly=True,
        path="/",
        expires=access_token_expires,
    )
    response.set_cookie(
        key="refresh_token",
        value=f"{refresh_token}",
        httponly=True,
        path="/",
        expires=refresh_token_expires,
    )
    return {"ok"}


@auth_router.post("/refresh")
async def refresh_token_regenerate(
    response: Response,
    db: db_dependency,
    old_refresh_token: str = Cookie(alias="refresh_token"),
):
    refresh_token_payload = decode_refresh_token(old_refresh_token)
    user_id = UUID(refresh_token_payload.get("id"))

    refresh_token_db = (
        db.query(models.RefreshTokens)
        .filter_by(user_id=user_id, refresh_token=old_refresh_token)
        .first()
    )

    if not refresh_token_db:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    db.query(models.RefreshTokens).filter_by(user_id=user_id).delete()

    user = get_user_by_id(user_id, db)
    access_token_expires, new_access_token = create_access_token(user)
    refresh_token_expires, new_refresh_token = create_refresh_token(user)

    refresh_token_db = models.RefreshTokens(
        refresh_token=new_refresh_token,
        user_id=user_id,
    )
    db.add(refresh_token_db)
    db.commit()

    response.set_cookie(
        key="access_token",
        value=f"Bearer {new_access_token}",
        httponly=True,
        path="/",
        expires=access_token_expires,
    )
    response.set_cookie(
        key="refresh_token",
        value=f"{new_refresh_token}",
        httponly=True,
        path="/",
        expires=refresh_token_expires,
    )
    return {"ok"}
