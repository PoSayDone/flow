from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Date
from sqlalchemy.dialects.postgresql import UUID
import datetime
from database import Base

class Users(Base):
    __tablename__ = 'users'
    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    username = Column(String, index=True)
    mail = Column(String, index=True)
    password_hash = Column(String)
    sex = Column(Boolean)
    birthdate = Column(Date)
    registration_date = Column(DateTime, default=datetime.datetime.utcnow, index=True)

class Matches(Base):
    __tablename__ = 'matches'
    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), index=True)
    interested_in_user_id = Column(UUID(as_uuid=True), index=True)

class Roles(Base):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True,autoincrement=True)
    role_name = Column(String, index=True)

class Interests(Base):
    __tablename__ = 'interests'
    id = Column(Integer, primary_key=True,autoincrement=True)
    interest_name = Column(String, index=True)

class Locations(Base):
    __tablename__ = 'locations'
    id = Column(Integer, primary_key=True, autoincrement=True)
    location_name = Column(String, index=True)

class UsersRoles(Base):
    __tablename__ = 'user_roles'
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), primary_key=True)
    role_id = Column(Integer, ForeignKey('roles.id'), primary_key=True)

class UsersInterests(Base):
    __tablename__ = 'user_interests'
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), primary_key=True)
    interest_id = Column(Integer, ForeignKey('interests.id'), primary_key=True)

class UsersLocations(Base):
    __tablename__ = 'user_locations'
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), primary_key=True)
    location_id = Column(Integer, ForeignKey('locations.id'), primary_key=True)

class UsersDepartures(Base):
    __tablename__ = 'user_departures'
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), primary_key=True)
    departure_id = Column(Integer, primary_key=True)

class Messages(Base):
    __tablename__ = 'messages'
    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    content_id = Column(UUID(as_uuid=True))
    from_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), index=True)
    to_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), index=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow, index=True)

class MessagesContents(Base):
    __tablename__ = 'message_contents'
    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    message_content = Column(String)
