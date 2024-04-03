from pydantic import BaseModel, EmailStr
from datetime import datetime, date
from typing import Optional
from uuid import UUID


class UserBase(BaseModel):
    id: UUID
    name: str
    mail: EmailStr
    password_hash: str
    occupation: str
    about: str
    sex: bool
    birthdate: date


class UserCreateRequest(BaseModel):
    id: UUID
    name: str
    mail: EmailStr
    password: str


class TokenBase(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class UserUpdate(BaseModel):
    name: Optional[str]
    mail: Optional[EmailStr]
    password_hash: Optional[str]
    occupation: Optional[str]
    about: Optional[str]
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


class CreateConversation(BaseModel):
    recipient_user_id: UUID


class NewMessage(BaseModel):
    content: str


class Profile(BaseModel):
    id: UUID
    name: Optional[str]
    mail: Optional[EmailStr]
    occupation: Optional[str]
    about: Optional[str]
    sex: Optional[bool]
    birthdate: Optional[date]
    user_status: Optional[bool]
    user_interests: Optional[list]
    user_trip_purposes: Optional[list] = None
    user_departures: Optional[list]
    user_arrivals: Optional[list]


class Solemate(BaseModel):
    id: UUID
    name: Optional[str]
    occupation: Optional[str]
    about: Optional[str]
    birthdate: Optional[date]
    trip_purposes: Optional[list]


class StatusDataEdit(BaseModel):
    user_status: bool
    user_departures: list[int]
    user_arrivals: list[int]
    user_trip_purposes: list[int]


class TagsEdit(BaseModel):
    tags: list[int]


class LocationsEdit(BaseModel):
    locations: list[int]
