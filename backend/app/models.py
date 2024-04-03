from typing import List
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Date,
    Table,
)
from sqlalchemy.dialects.postgresql import UUID, array
import datetime

from sqlalchemy.orm import Mapped, backref, mapped_column, relationship

from app.schema import UserBase
from .database import Base


conversation_participant = Table(
    "conversation_participant",
    Base.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("conversation_id", ForeignKey("conversations.id"), primary_key=True),
)


class Users(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    name = Column(String, index=True)
    occupation = Column(String, index=True)
    about = Column(String, index=True)
    mail = Column(String, index=True)
    password_hash = Column(String)
    sex = Column(Boolean)
    birthdate = Column(Date)
    registration_date = Column(DateTime, default=datetime.datetime.utcnow, index=True)
    conversations: Mapped[List["Conversation"]] = relationship(
        secondary=conversation_participant, back_populates="users"
    )
    messages: Mapped[List["Message"]] = relationship(back_populates="sender")
    status = Column(Boolean, default=True)


class RefreshTokens(Base):
    __tablename__ = "refresh_tokens"
    user_id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    refresh_token = Column(String)
    expires_at = Column(DateTime)


class Matches(Base):
    __tablename__ = "matches"
    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), index=True)
    liked_user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), index=True)
    mutual = Column(Boolean, default=False)


class Roles(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True, autoincrement=True)
    role_name = Column(String, index=True)


class Interests(Base):
    __tablename__ = "interests"
    id = Column(Integer, primary_key=True, autoincrement=True)
    interest_name = Column(String, index=True)


class TripPurposes(Base):
    __tablename__ = "trip_purposes"
    id = Column(Integer, primary_key=True, autoincrement=True)
    purpose_name = Column(String, index=True)


class Departures(Base):
    __tablename__ = "departures"
    id = Column(Integer, primary_key=True, autoincrement=True)
    location_name = Column(String, index=True)


class Arrivals(Base):
    __tablename__ = "arrivals"
    id = Column(Integer, primary_key=True, autoincrement=True)
    location_name = Column(String, index=True)


class UsersRoles(Base):
    __tablename__ = "users_roles"
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True)
    role_id = Column(Integer, ForeignKey("roles.id"), primary_key=True)


class UsersInterests(Base):
    __tablename__ = "users_interests"
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True)
    interest_id = Column(Integer, ForeignKey("interests.id"), primary_key=True)


class UsersTripPurposes(Base):
    __tablename__ = "users_trip_purposes"
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True)
    purpose_id = Column(Integer, ForeignKey("trip_purposes.id"), primary_key=True)


class UsersDepartures(Base):
    __tablename__ = "users_departures"
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True)
    location_id = Column(Integer, ForeignKey("departures.id"), primary_key=True)


class UsersArrivals(Base):
    __tablename__ = "users_arrivals"
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True)
    location_id = Column(Integer, ForeignKey("arrivals.id"), primary_key=True)


class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow())
    updated_at = Column(DateTime, default=datetime.datetime.utcnow())
    is_deleted = Column(Boolean, default=False)

    users: Mapped[List["Users"]] = relationship(
        secondary=conversation_participant, back_populates="conversations"
    )
    messages: Mapped[List["Message"]] = relationship(back_populates="conversation")


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, autoincrement=True)
    body = Column(String)
    image = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow())

    conversation_id: Mapped[int] = mapped_column(ForeignKey("conversations.id"))
    conversation: Mapped["Conversation"] = relationship(back_populates="messages")

    sender_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))
    sender: Mapped["Users"] = relationship(back_populates="messages")
