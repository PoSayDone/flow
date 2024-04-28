from typing import Annotated
from uuid import UUID
from fastapi import Depends, HTTPException, status
from passlib.context import CryptContext
from pydantic import EmailStr
from app import models

from app.auth.helpers import decode_access_token
from app.models import Users
from app.dependencies import db_dependency
from app.utils import OAuth2PasswordBearerWithCookie

oauth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="auth/login")
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)], db: db_dependency
) -> models.Users | None:
    try:
        payload = decode_access_token(token)
        mail: str = str(payload.get("sub"))
        id: UUID = UUID(payload.get("id"))
        if mail is None or id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate user",
            )
        user: Users = db.get(models.Users, id)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate user",
            )
        return user
    except AttributeError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user"
        )


def authneticate_user(mail: EmailStr, password: str, db: db_dependency):
    user = db.query(Users).filter(Users.mail == mail).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user"
        )
    if not bcrypt_context.verify(password, str(user.password_hash)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user"
        )
    return user


def get_user_by_mail(mail, db: db_dependency):
    return db.query(models.Users).filter(models.Users.mail == mail).first()


def get_user_by_id(id, db: db_dependency):
    return db.query(models.Users).filter(models.Users.id == id).first()


user_dependency = Annotated[models.Users, Depends(get_current_user)]
