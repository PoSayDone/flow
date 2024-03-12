import logging
import uuid

from sqlalchemy import and_, exists, join
from app import auth
from fastapi.security import OAuth2PasswordBearer
from uuid import UUID
from passlib.context import CryptContext
from fastapi import FastAPI, HTTPException, Depends
from typing import  Annotated, List
from . import schema, models
from .database import engine, SessionLocal
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from fastapi.logger import logger
import logging

gunicorn_logger = logging.getLogger('gunicorn.error')
logger.handlers = gunicorn_logger.handlers
if __name__ != "main":
    logger.setLevel(gunicorn_logger.level)
else:
    logger.setLevel(logging.DEBUG)

app = FastAPI(root_path="/api")
app.include_router(auth.router)
models.Base.metadata.create_all(bind=engine)

# Assuming app is your FastAPI application instance
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173","http://localhost:8000","http://localhost","http://127.0.0.1", "http://0.0.0.0", "http://192.168.1.129"],  # Add your frontend URL here
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(auth.get_current_user)]

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.get("/profile/")
async def get_profile(user: user_dependency, db: db_dependency):
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user_db = db.get(models.Users, user['id'])
    result = schema.Profile(
        id = user_db.id,
        name = user_db.name,
        mail = user_db.mail,
        occupation=user_db.occupation,
        about=user_db.about,
        sex=user_db.sex,
        birthdate=user_db.birthdate,
        interests=list(map(lambda interest: interest.interest_id, db.query(models.UsersInterests).filter(models.UsersInterests.user_id == user_db.id).all())),
        trip_purposes=list(map(lambda purpose: purpose.purpose_id,db.query(models.UsersTripPurposes).filter(models.UsersTripPurposes.user_id == user_db.id).all()))
    )
    return result

@app.get("/profile/{user_id}")
async def get_profile_w_id(user_id: UUID, db: db_dependency):
    user_db = db.get(models.Users, user_id)
    if not user_db:
        raise HTTPException(status_code=404, detail="User not found")
    result = schema.Profile(
        id = user_db.id,
        name = user_db.name,
        mail = user_db.mail,
        occupation=user_db.occupation,
        about=user_db.about,
        sex=user_db.sex,
        birthdate=user_db.birthdate,
        interests=list(map(lambda interest: interest.interest_id, db.query(models.UsersInterests).filter(models.UsersInterests.user_id == user_db.id).all())),
        trip_purposes=list(map(lambda purpose: purpose.purpose_id,db.query(models.UsersTripPurposes).filter(models.UsersTripPurposes.user_id == user_db.id).all()))
    )
    return result

#SELECT * FROM table_name;
@app.get("/users/")
async def get_users(db: db_dependency):
    result = db.query(models.Users).all()
    if not result:
        raise HTTPException(status_code=404, detail="No users found")
    return result

@app.get("/find_solemates/{count}/")
async def get_user_solemates(count: int, db: db_dependency):
    users = db.query(models.Users).limit(count).all();
    if not users:
        raise HTTPException(status_code=404, detail="No solemates found")
    result = list(map(lambda user: schema.Solemate(
        id=user.id,
        name=user.name,
        occupation=user.occupation,
        about=user.about,
        birthdate=user.birthdate,
        trip_purposes=list(map(lambda purpose: purpose.purpose_id,db.query(models.UsersTripPurposes).filter(models.UsersTripPurposes.user_id == user.id).all()))
    ), users))
    return result

@app.get("/solemates/{count}")
async def get_soulmates(count:int, db: db_dependency, user: user_dependency):
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user_db = db.get(models.Users, user['id'])
    current_user_interests = [interest[0] for interest in db.query(models.UsersInterests.interest_id).filter(models.UsersInterests.user_id == user_db.id).all()]
    current_user_purposes = [purpose[0] for purpose in db.query(models.UsersTripPurposes.purpose_id).filter(models.UsersTripPurposes.user_id == user_db.id).all()]

    # Находим других пользователей с теми же интересами и целями поездки
    matching_users = db.query(models.Users).\
        join(models.UsersInterests, models.Users.id == models.UsersInterests.user_id).\
        join(models.UsersTripPurposes, models.Users.id == models.UsersTripPurposes.user_id).\
        filter(and_(models.UsersInterests.interest_id.in_(current_user_interests),
                    models.UsersTripPurposes.purpose_id.in_(current_user_purposes),
                    models.Users.id != user_db.id)).limit(count).all()

    result = list(map(lambda user: schema.Solemate(
        id=user.id,
        name=user.name,
        occupation=user.occupation,
        about=user.about,
        birthdate=user.birthdate,
        trip_purposes=list(map(lambda purpose: purpose.purpose_id,db.query(models.UsersTripPurposes).filter(models.UsersTripPurposes.user_id == user.id).all()))
    ), matching_users))

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
async def add_user(user: schema.UserBase, db: db_dependency):
    user = models.Users(
        id=user.id,
        name=user.name,
        mail=user.mail,
        password_hash=user.password_hash,
        sex=user.sex,
        birthdate=user.birthdate,
    )
    if (db.query(models.Users).filter(models.Users.mail == user.mail).all()):
        raise HTTPException(status_code=409, detail="User with this mail already exisits")
    db.add(user)
    db.commit()
    return {"ok": True}

# UPDATE table_name
# SET column1 = value1, column2 = value2, ...
# WHERE condition;
@app.put("/user/")
async def update_user(user: user_dependency, user_update: schema.UserUpdateBase, db: db_dependency):
    if not user:
        raise HTTPException(status_code=404, detail="Not authorized")
    db_user = db.query(models.Users).filter(models.Users.id == user['id']).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    for field, value in user_update.dict(exclude_unset=True).items():
        setattr(db_user, field, value)
    db.commit()
    return {"message": "User updated successfully"}

@app.post("/trip_purposes/")
async def add_trip_purpose(purpose: schema.InfoTableBase, db: db_dependency):
    purpose = models.TripPurposes(
        purpose_name = purpose.name,
    )
    db.add(purpose)
    db.commit()
    return {"ok": True}

@app.get("/trip_purposes/")
async def get_trip_purpose(db: db_dependency):
    result = db.query(models.TripPurposes).all()
    if not result:
        raise HTTPException(status_code=404, detail="No trip purposes found")
    return result

@app.post("/interests/")
async def add_interest(interest: schema.InfoTableBase, db: db_dependency):
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
async def add_role(role: schema.InfoTableBase, db: db_dependency):
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
async def add_location(location: schema.InfoTableBase, db: db_dependency):
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

@app.put("/match/{interested_in_user_id}")
async def add_match(interested_in_user_id: UUID, user: user_dependency, db: db_dependency):
    if not user:
        raise HTTPException(status_code=401, detail="Not authorized")
    match = models.Matches(
        id = uuid.uuid4(),
        user_id = user['id'],
        interested_in_user_id = interested_in_user_id
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
async def add_user_location(data: schema.PivotTableBase, db: db_dependency):
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
async def add_user_departure(object: schema.PivotTableBase, db: db_dependency):
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

@app.get("/user_trip_purposes/")
async def get_user_trip_purposes(user: user_dependency, db: db_dependency):
    if not user:
        raise HTTPException(status_code=401, detail="Not authorized")
    result = db.query(models.UsersTripPurposes).filter(models.UsersTripPurposes.user_id == user['id']).all()
    if not result:
        raise HTTPException(status_code=404, detail="No trip purposes found")
    return result

@app.put("/user_trip_purposes/{purpose_id}")
async def add_user_trip_purpose(purpose_id: int, user: user_dependency, db: db_dependency):
    user_trip_purpose = models.UsersTripPurposes(
        user_id = user['id'],
        purpose_id = purpose_id
    )
    db.add(user_trip_purpose)
    db.commit()
    return {"ok": True}

@app.put("/user_trip_purposes/{user_id}/{purpose_id}")
async def add_user_trip_purpose_by_id(purpose_id: int, user_id: UUID, db: db_dependency):
    user_trip_purpose = models.UsersTripPurposes(
        user_id = user_id,
        purpose_id = purpose_id
    )
    db.add(user_trip_purpose)
    db.commit()
    return {"ok": True}

@app.delete("/user_trip_purposes/{purpose_id}")
async def delete_user_trip_purpose(user: user_dependency, purpose_id: int, db: db_dependency):
    if not user:
        raise HTTPException(status_code=401, detail="Not authorized")
    user_trip_purpose = db.get(models.UsersTripPurposes, (user['id'], purpose_id))
    if not user_trip_purpose:
        raise HTTPException(status_code=404, detail="Purpose not found")
    db.delete(user_trip_purpose)
    db.commit()
    return {"ok": True}

@app.put("/user_interests/{user_id}/{interest_id}")
async def add_user_interest_by_id(user_id: UUID, interest_id: int, db: db_dependency):
    user_interest = models.UsersInterests(
        user_id = user_id,
        interest_id = interest_id
    )
    db.add(user_interest)
    db.commit()
    return {"ok": True}

@app.put("/user_interests/{interest_id}")
async def add_user_interest(interest_id: int, user: user_dependency, db: db_dependency):
    user_interest = models.UsersInterests(
        user_id = user['id'],
        interest_id = interest_id
    )
    db.add(user_interest)
    db.commit()
    return {"ok": True}

@app.delete("/user_interests/{interest_id}")
async def delete_user_interest(user: user_dependency, interest_id: int, db: db_dependency):
    if not user:
        raise HTTPException(status_code=401, detail="Not authorized")
    user_interest = db.get(models.UsersInterests, (user['id'], interest_id))
    if not user_interest:
        raise HTTPException(status_code=404, detail="Interest not found")
    db.delete(user_interest)
    db.commit()
    return {"ok": True}

@app.get("/user_interests/")
async def get_user_interests(user: user_dependency, db: db_dependency):
    if not user:
        raise HTTPException(status_code=401, detail="Not authorized")
    result = db.query(models.UsersInterests).filter(models.UsersInterests.user_id == user['id']).all()
    if not result:
        raise HTTPException(status_code=404, detail="No interests found")
    return result

@app.post("/users_roles/")
async def add_user_role(object: schema.PivotTableBase, db: db_dependency):
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
