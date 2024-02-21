from pydantic import BaseModel, EmailStr
from datetime import datetime, date
from typing import  Annotated, Optional, List
from uuid import UUID

class UserBase(BaseModel):
    id: UUID
    username: str
    mail: EmailStr
    password_hash: str
    sex: bool
    birthdate: date

class UserUpdateBase(BaseModel):
    id: UUID
    username: Optional[str]
    mail: Optional[EmailStr]
    password_hash: Optional[str]
    sex: Optional[bool]
    birthdate: Optional[date]

class MatchBase(BaseModel):
    id: UUID
    user_id: UUID
    interested_in_user_id: UUID

class InfoTableBase(BaseModel):
    name: str

class PivotTableBase(BaseModel):
    user_id: UUID
    id: int

class MessageBase(BaseModel):
    id: UUID
    content_id: UUID
    from_id: UUID
    to_id: UUID
    created_at: datetime
    updated_at: datetime

class MessageContentBase(BaseModel):
    id: UUID
    message_content: str

class Token(BaseModel):
    access_token: str
    token_type: str
