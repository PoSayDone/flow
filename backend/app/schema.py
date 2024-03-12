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
    token_type: str

class UserUpdateBase(BaseModel):
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

class Profile(BaseModel):
    id:            UUID
    name:          Optional[str     ]
    mail:          Optional[EmailStr]
    occupation:    Optional[str     ]
    about:         Optional[str     ]
    sex:           Optional[bool    ]
    birthdate:     Optional[date    ]
    interests:     Optional[list]
    trip_purposes: Optional[list] = None

class Solemate(BaseModel):
    id:         UUID
    name:       Optional[str     ]
    occupation: Optional[str     ]
    about:      Optional[str     ]
    birthdate:     Optional[date    ]
    trip_purposes:  Optional[list]
