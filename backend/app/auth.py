from datetime import datetime, timedelta
import logging
from typing import Annotated
from uuid import UUID
from jose import jwt, JWTError
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from pydantic import EmailStr
from sqlalchemy.orm import Session

gunicorn_logger = logging.getLogger('gunicorn.error')

from app.models import Users
from app.schema import TokenBase, UserCreateRequest
from .database import SessionLocal

SECRET_KEY = "4bad42439cea6743a225bc13fcaacf0bbf637edbb197d96611f2b40c36ce724c"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, user_create_request: UserCreateRequest):
    user_create_model = Users(
        id = user_create_request.id,
        name=user_create_request.name,
        mail = user_create_request.mail,
        password_hash = bcrypt_context.hash(user_create_request.password)
    )
    db.add(user_create_model)
    db.commit()

@router.post("/token", response_model=TokenBase)
async def login_for_access_token(db: db_dependency, form_data: OAuth2PasswordRequestForm = Depends()):
    authenticated_user = authneticate_user(form_data.username, form_data.password, db)
    if not authenticated_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user")
    token = create_access_token(authenticated_user.mail, authenticated_user.id, timedelta(minutes=30))
    return {'access_token': token, 'token_type': 'bearer'}

def authneticate_user(mail: EmailStr, password: str, db: db_dependency):
    user = db.query(Users).filter(Users.mail == mail).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.password_hash):
        return False
    return user

def create_access_token(mail: EmailStr, user_id: UUID, expires_date: timedelta):
    encode = {'sub':mail, 'id': user_id.__str__()}
    expires = datetime.utcnow() + expires_date
    encode.update({'exp': expires})
    return jwt.encode(encode, key=SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        mail: str = str(payload.get('sub'))
        id: UUID = UUID(payload.get('id'))
        if mail is None or id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user")
        return {'mail': mail, 'id': id.__str__()}
    except JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user")
