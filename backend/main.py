from fastapi import FastAPI, HTTPException, Depends, Path
from pydantic import BaseModel, EmailStr
from typing import  Annotated, Optional, List
from datetime import datetime, date
from uuid import UUID
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

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

class MessageContentBase:
    id: UUID
    message_content: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

#SELECT * FROM table_name;
@app.get("/users/")
async def get_users(db: db_dependency):
    result = db.query(models.Users).all()
    if not result:
        raise HTTPException(status_code=404, detail="No users found")
    return result

#SELECT * FROM table_name WHERE condition;
@app.get("/users/{user_id}")
async def get_user(user_id: UUID, db: db_dependency):
    result = db.get(models.Users, user_id)
    if not result:
        raise HTTPException(status_code=404, detail="User not found")
    return result

#DELETE FROM table_name WHERE condition;
@app.delete("/users/{user_id}")
async def delete_user(user_id: UUID, db: db_dependency):
    user = db.get(models.Users, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"ok": True}

#INSERT INTO TABLE_NAME VALUES (значение1, значение2, значение3,... значение N);
@app.post("/users/")
async def add_user(user: UserBase, db: db_dependency):
    user = models.Users(
        id=user.id,
        username=user.username,
        mail=user.mail,
        password_hash=user.password_hash,
        sex=user.sex,
        birthdate=user.birthdate,
    )
    if (db.query(models.Users).filter(models.Users.username == user.username).all()):
        raise HTTPException(status_code=409, detail="User with this username already exists")
    if (db.query(models.Users).filter(models.Users.mail == user.mail).all()):
        raise HTTPException(status_code=409, detail="User with this mail already exisits")
    db.add(user)
    db.commit()
    return {"ok": True}

# UPDATE table_name
# SET column1 = value1, column2 = value2, ...
# WHERE condition;
@app.put("/users/")
async def update_user(user: UserUpdateBase, db: db_dependency):
    if not user.id:
        raise HTTPException(status_code=404, detail="User not found")
    db.query(models.Users).\
    filter(models.Users.id == user.id).\
    update(dict(user))
    db.commit()
    return {"message": "User updated successfully"}


@app.post("/interests/")
async def add_interest(interest: InfoTableBase, db: db_dependency):
    interest = models.Interests(
        interest_name = interest.name,
    )
    db.add(interest)
    db.commit()
    return {"ok": True}

@app.get("/interests/")
async def get_interests(db: db_dependency):
    result = db.query(models.Interests).all()
    if not result:
        raise HTTPException(status_code=404, detail="No interests found")
    return result

@app.delete("/interests/{interest_id}")
async def delete_interest(interest_id: int, db: db_dependency):
    interest = db.get(models.Interests, interest_id)
    if not interest:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(interest)
    db.commit()
    return {"ok": True}

@app.post("/roles/")
async def add_role(role: InfoTableBase, db: db_dependency):
    role = models.Roles(
        role_name = role.name,
    )
    db.add(role)
    db.commit()
    return {"ok": True}

@app.get("/roles/")
async def get_roles(db: db_dependency):
    result = db.query(models.Roles).all()
    if not result:
        raise HTTPException(status_code=404, detail="No roles found")
    return result

@app.delete("/roles/{role_id}")
async def delete_role(role_id: int, db: db_dependency):
    role = db.get(models.Roles, role_id)
    if not role:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(role)
    db.commit()
    return {"ok": True}

@app.post("/locations/")
async def add_location(location: InfoTableBase, db: db_dependency):
    location = models.Locations(
        location_name = location.name,
    )
    db.add(location)
    db.commit()
    return {"ok": True}

@app.get("/locations/")
async def get_locations(db: db_dependency):
    result = db.query(models.Locations).all()
    if not result:
        raise HTTPException(status_code=404, detail="No locations found")
    return result

@app.delete("/locations/{location_id}")
async def delete_location(location_id: int, db: db_dependency):
    location = db.get(models.Locations, location_id)
    if not location:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(location)
    db.commit()
    return {"ok": True}

@app.post("/matches/")
async def add_match(match: MatchBase,db: db_dependency):
    match = models.Matches(
        id = match.id,
        user_id = match.user_id,
        interested_in_user_id = match.interested_in_user_id
    )
    db.add(match)
    db.commit()
    return {"ok": True}

@app.get("/matches/")
async def get_matches(db: db_dependency):
    result = db.query(models.Matches).all()
    if not result:
        raise HTTPException(status_code=404, detail="No locations found")
    return result

@app.post("/users_locations/")
async def add_user_location(data: PivotTableBase, db: db_dependency):
    data = models.UsersLocations(
        user_id = data.user_id,
        location_id = data.id
    )
    db.add(data)
    db.commit()
    return {"ok": True}

@app.delete("/users_locations/{user_id}/{location_id}")
async def delete_user_location(user_id: UUID, location_id: int, db: db_dependency):
    user_location = db.get(models.UsersLocations, (user_id, location_id))
    if not user_location:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user_location)
    db.commit()
    return {"ok": True}

@app.get("/users_locations/")
async def get_users_locations(db: db_dependency):
    result = db.query(models.UsersLocations).all()
    if not result:
        raise HTTPException(status_code=404, detail="No locations found")
    return result

@app.post("/users_departures/")
async def add_user_departure(object: PivotTableBase, db: db_dependency):
    object = models.UsersDepartures(
        user_id = object.user_id,
        id = object.id
    )
    db.add(models)
    db.commit()
    return {"ok": True}

@app.delete("/users_departures/{user_id}/{departure_id}")
async def delete_user_departure(user_id: UUID, departure_id: int, db: db_dependency):
    user_departure = db.get(models.UsersDepartures, (user_id, departure_id))
    if not user_departure:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user_departure)
    db.commit()
    return {"ok": True}

@app.get("/users_departures/")
async def get_users_departures(db: db_dependency):
    result = db.query(models.UsersDepartures).all()
    if not result:
        raise HTTPException(status_code=404, detail="No departures found")
    return result

@app.post("/users_interests/")
async def add_user_interest(object: PivotTableBase, db: db_dependency):
    object = models.UsersInterests(
        user_id = object.user_id,
        id = object.id
    )
    db.add(models)
    db.commit()
    return {"ok": True}

@app.delete("/users_interests/{user_id}/{interest_id}")
async def delete_user_interest(user_id: UUID, interest_id: int, db: db_dependency):
    user_interest = db.get(models.UsersInterests, (user_id, interest_id))
    if not user_interest:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user_interest)
    db.commit()
    return {"ok": True}

@app.get("/users_interests/")
async def get_users_interests(db: db_dependency):
    result = db.query(models.UsersInterests).all()
    if not result:
        raise HTTPException(status_code=404, detail="No interests found")
    return result

@app.post("/users_roles/")
async def add_user_role(object: PivotTableBase, db: db_dependency):
    object = models.UsersRoles(
        user_id = object.user_id,
        id = object.id
    )
    db.add(models)
    db.commit()
    return {"ok": True}

@app.delete("/users_roles/{user_id}/{role_id}")
async def delete_user_role(user_id: UUID, role_id: int, db: db_dependency):
    user_role = db.get(models.UsersRoles, (user_id, role_id))
    if not user_role:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user_role)
    db.commit()
    return {"ok": True}

@app.get("/users_roles/")
async def get_users_roles(db: db_dependency):
    result = db.query(models.UsersRoles).all()
    if not result:
        raise HTTPException(status_code=404, detail="No roles found")
    return result

@app.post('/users_in/')
async def get_users_from_locations(locations_ids: List[int], db: db_dependency):
    result = db.query(models.UsersLocations)\
        .filter(models.UsersLocations.location_id.in_(locations_ids))\
        .group_by(models.UsersLocations.location_id, models.UsersLocations.user_id).all()
    if not result:
        raise HTTPException(status_code=404, detail="No users found in specified location")
    return result
