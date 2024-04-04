from pydantic import BaseModel, ConfigDict, EmailStr, field_serializer, validator
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
    occupation: Optional[str]
    about: Optional[str]
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


class Interest(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    interest_name: str


class TripPurpose(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    purpose_name: str


class Departure(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    departure_name: str


class Arrival(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    arrival_name: str


class Profile(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: Optional[str]
    mail: Optional[EmailStr]
    occupation: Optional[str]
    about: Optional[str]
    sex: Optional[bool]
    birthdate: Optional[date]
    status: Optional[bool]
    interests: list[Interest]
    trip_purposes: list[TripPurpose]
    departures: list[Departure]
    arrivals: list[Arrival]

    @field_serializer("interests")
    def serialize_interests(self, interests: Optional[list[Interest]], _info):
        if interests:
            return map(lambda x: x.id, interests)
        else:
            return []

    @field_serializer("trip_purposes")
    def serialize_trip_purposes(
        self, trip_purposes: Optional[list[TripPurpose]], _info
    ):
        if trip_purposes:
            return map(lambda x: x.id, trip_purposes)
        else:
            return []

    @field_serializer("departures")
    def serialize_departures(self, departures: Optional[list[Departure]], _info):
        if departures:
            return map(lambda x: x.id, departures)
        else:
            return []

    @field_serializer("arrivals")
    def serialize_arrivals(self, arrivals: Optional[list[Arrival]], _info):
        if arrivals:
            return map(lambda x: x.id, arrivals)
        else:
            return []


class Soulmate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: Optional[str]
    occupation: Optional[str]
    about: Optional[str]
    birthdate: Optional[date]
    trip_purposes: Optional[list]

    @field_serializer("trip_purposes")
    def serialize_trip_purposes(
        self, trip_purposes: Optional[list[TripPurpose]], _info
    ):
        if trip_purposes:
            return map(lambda x: x.id, trip_purposes)
        else:
            return []


class SoulmatesResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    soulmates: list[Soulmate]


class StatusDataEdit(BaseModel):
    user_status: bool
    user_departures: list[int]
    user_arrivals: list[int]
    user_trip_purposes: list[int]


class TagsEdit(BaseModel):
    tags: list[int]


class LocationsEdit(BaseModel):
    locations: list[int]
