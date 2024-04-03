from uuid import UUID
import uuid
from fastapi import APIRouter, HTTPException
from sqlalchemy import and_, delete, insert, or_

from app import models, schema
from app.chat.services import create_conversation_db
from app.routes.auth import user_dependency
from app.dependencies import db_dependency


router = APIRouter(prefix="/user", tags=["user"])


@router.delete("/{user_id}")
async def delete_user(user_id: UUID, db: db_dependency):
    user = db.get(models.Users, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"ok": True}


@router.patch("/")
async def update_user(
    user: user_dependency, user_update: schema.UserUpdate, db: db_dependency
):
    if not user:
        raise HTTPException(status_code=404, detail="Not authorized")
    db_user = db.query(models.Users).filter(models.Users.id == user.id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    for field, value in user_update.dict(exclude_unset=True).items():
        setattr(db_user, field, value)
    db.commit()
    return {"message": "User updated successfully"}


@router.get("/solemates/{count}")
async def get_soulmates(count: int, db: db_dependency, user: user_dependency):
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    current_user_interests = [
        interest[0]
        for interest in db.query(models.UsersInterests.interest_id)
        .filter(models.UsersInterests.user_id == user.id)
        .all()
    ]
    current_user_purposes = [
        purpose[0]
        for purpose in db.query(models.UsersTripPurposes.purpose_id)
        .filter(models.UsersTripPurposes.user_id == user.id)
        .all()
    ]

    # Находим других пользователей с теми же интересами и целями поездки
    matching_users = (
        db.query(models.Users)
        .join(models.UsersInterests, models.Users.id == models.UsersInterests.user_id)
        .join(
            models.UsersTripPurposes,
            models.Users.id == models.UsersTripPurposes.user_id,
        )
        .filter(
            and_(
                models.UsersInterests.interest_id.in_(current_user_interests),
                models.UsersTripPurposes.purpose_id.in_(current_user_purposes),
                models.Users.id != user.id,
            )
        )
        .limit(count)
        .all()
    )

    result = list(
        map(
            lambda user: schema.Solemate(
                id=user.id,
                name=user.name,
                occupation=user.occupation,
                about=user.about,
                birthdate=user.birthdate,
                trip_purposes=list(
                    map(
                        lambda purpose: purpose.purpose_id,
                        db.query(models.UsersTripPurposes)
                        .filter(models.UsersTripPurposes.user_id == user.id)
                        .all(),
                    )
                ),
            ),
            matching_users,
        )
    )

    return result


### status_data


@router.patch("/status_data/edit", tags=["status"])
async def edit_user_status_data(
    user: user_dependency,
    db: db_dependency,
    edit: schema.StatusDataEdit,
):
    if not user:
        raise HTTPException(status_code=404, detail="Not authorized")
    user.status = edit.user_status
    db.execute(
        delete(models.UsersDepartures).where(models.UsersDepartures.user_id == user.id)
    )
    db.execute(
        delete(models.UsersArrivals).where(models.UsersArrivals.user_id == user.id)
    )
    db.execute(
        delete(models.UsersTripPurposes).where(
            models.UsersTripPurposes.user_id == user.id
        )
    )
    db.execute(
        insert(models.UsersDepartures).values(
            [
                {"user_id": user.id, "location_id": location_id}
                for location_id in edit.user_departures
            ]
        )
    )
    db.execute(
        insert(models.UsersArrivals).values(
            [
                {"user_id": user.id, "location_id": location_id}
                for location_id in edit.user_arrivals
            ]
        )
    )
    db.execute(
        insert(models.UsersTripPurposes).values(
            [
                {"user_id": user.id, "purpose_id": purpose_id}
                for purpose_id in edit.user_trip_purposes
            ]
        )
    )
    db.commit()
    return {"ok": True}


### profile


@router.get("/profile")
async def get_profile(user: user_dependency, db: db_dependency):
    if not user:
        raise HTTPException(status_code=401, detail="Not authorized")
    if user:
        result = schema.Profile(
            id=user.id,
            name=user.name,
            mail=user.mail,
            occupation=user.occupation,
            about=user.about,
            sex=user.sex,
            birthdate=user.birthdate,
            user_status=user.status,
            user_interests=list(
                map(
                    lambda interest: interest.interest_id,
                    db.query(models.UsersInterests)
                    .filter(models.UsersInterests.user_id == user.id)
                    .all(),
                )
            ),
            user_trip_purposes=list(
                map(
                    lambda purpose: purpose.purpose_id,
                    db.query(models.UsersTripPurposes)
                    .filter(models.UsersTripPurposes.user_id == user.id)
                    .all(),
                )
            ),
            user_departures=list(
                map(
                    lambda departure: departure.location_id,
                    db.query(models.UsersDepartures)
                    .filter(models.UsersDepartures.user_id == user.id)
                    .all(),
                )
            ),
            user_arrivals=list(
                map(
                    lambda arrival: arrival.location_id,
                    db.query(models.UsersArrivals)
                    .filter(models.UsersArrivals.user_id == user.id)
                    .all(),
                )
            ),
        )
        return result


@router.get("/profile/{user_id}")
async def get_profile_w_id(user_id: UUID, db: db_dependency):
    user_db = db.get(models.Users, user_id)
    if not user_db:
        raise HTTPException(status_code=404, detail="User not found")
    result = schema.Profile(
        id=user_db.id,
        name=user_db.name,
        mail=user_db.mail,
        occupation=user_db.occupation,
        about=user_db.about,
        sex=user_db.sex,
        birthdate=user_db.birthdate,
        user_interests=list(
            map(
                lambda interest: interest.interest_id,
                db.query(models.UsersInterests)
                .filter(models.UsersInterests.user_id == user_db.id)
                .all(),
            )
        ),
        user_trip_purposes=list(
            map(
                lambda purpose: purpose.purpose_id,
                db.query(models.UsersTripPurposes)
                .filter(models.UsersTripPurposes.user_id == user_db.id)
                .all(),
            )
        ),
        user_departures=list(
            map(
                lambda departure: departure.location_id,
                db.query(models.UsersDepartures)
                .filter(models.UsersDepartures.user_id == user_db.id)
                .all(),
            )
        ),
        user_arrivals=list(
            map(
                lambda arrival: arrival.location_id,
                db.query(models.UsersArrivals)
                .filter(models.UsersArrivals.user_id == user_db.id)
                .all(),
            )
        ),
    )
    return result


### roles


@router.get("/roles")
async def get_users_roles(db: db_dependency):
    result = db.query(models.UsersRoles).all()
    if not result:
        raise HTTPException(status_code=404, detail="No roles found")
    return result


@router.post("/roles")
async def add_user_role(object: schema.PivotTableBase, db: db_dependency):
    object = models.UsersRoles(user_id=object.user_id, id=object.id)
    db.add(models)
    db.commit()
    return {"ok": True}


@router.delete("/roles/{user_id}/{role_id}")
async def delete_user_role(user_id: UUID, role_id: int, db: db_dependency):
    user_role = db.get(models.UsersRoles, (user_id, role_id))
    if not user_role:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user_role)
    db.commit()
    return {"ok": True}


### matches


@router.post("/match/{interested_in_user_id}", tags=["matches"])
async def add_match(liked_user_id: UUID, user: user_dependency, db: db_dependency):
    if not user:
        raise HTTPException(status_code=401, detail="Not authorized")

    recepient = db.get(models.Users, liked_user_id)

    if not recepient:
        raise HTTPException(status_code=404, detail="Recepient not found")

    existing_match = (
        db.query(models.Matches)
        .filter(
            or_(
                and_(
                    models.Matches.user_id == user.id,
                    models.Matches.liked_user_id == recepient.id,
                ),
                and_(
                    models.Matches.user_id == recepient.id,
                    models.Matches.liked_user_id == user.id,
                ),
            )
        )
        .first()
    )
    print(existing_match)

    if existing_match:
        if existing_match.user_id != user.id:
            existing_match.mutual = True
    else:
        match = models.Matches(user_id=user.id, liked_user_id=liked_user_id)
        db.add(match)
    db.commit()
    await create_conversation_db(db, user, recepient)

    return {"ok": True}


@router.get("/matches", tags=["matches"])
async def get_matches(db: db_dependency):
    result = db.query(models.Matches).all()
    if not result:
        raise HTTPException(status_code=404, detail="No locations found")
    return result


### interests


# @router.post("/interests/{user_id}/{interest_id}")
# async def add_user_interest_by_id(user_id: UUID, interest_id: int, db: db_dependency):
#     user_interest = models.UsersInterests(user_id=user_id, interest_id=interest_id)
#     db.add(user_interest)
#     db.commit()
#     return {"ok": True}


@router.get("/interests", tags=["interests"])
async def get_user_interests(user: user_dependency, db: db_dependency):
    if not user:
        raise HTTPException(status_code=401, detail="Not authorized")
    result = (
        db.query(models.UsersInterests)
        .filter(models.UsersInterests.user_id == user.di)
        .all()
    )
    if not result:
        raise HTTPException(status_code=404, detail="No interests found")
    return result


@router.post("/interests/{interest_id}", tags=["interests"])
async def add_user_interest(interest_id: int, user: user_dependency, db: db_dependency):
    user_interest = models.UsersInterests(user_id=user.id, interest_id=interest_id)
    db.add(user_interest)
    db.commit()
    return {"ok": True}


@router.patch("/interests/edit", tags=["interests"])
async def edit_user_interests(
    user: user_dependency, edit: schema.TagsEdit, db: db_dependency
):
    if not user:
        raise HTTPException(status_code=404, detail="Not authorized")
    db.execute(
        delete(models.UsersInterests).where(models.UsersInterests.user_id == user.id)
    )
    db.execute(
        insert(models.UsersInterests).values(
            [
                {"user_id": user.id, "interest_id": interest_id}
                for interest_id in edit.tags
            ]
        )
    )
    db.commit()
    return {"ok": True}


@router.delete("/interests/{interest_id}", tags=["interests"])
async def delete_user_interest(
    user: user_dependency, interest_id: int, db: db_dependency
):
    if not user:
        raise HTTPException(status_code=401, detail="Not authorized")
    user_interest = db.get(models.UsersInterests, (user.id, interest_id))
    if not user_interest:
        raise HTTPException(status_code=404, detail="Interest not found")
    db.delete(user_interest)
    db.commit()
    return {"ok": True}


### trip purposes


# @router.post("/trip_purposes/{user_id}/{purpose_id}")
# async def add_user_trip_purpose_by_id(
#     purpose_id: int, user_id: UUID, db: db_dependency
# ):
#     user_trip_purpose = models.UsersTripPurposes(user_id=user_id, purpose_id=purpose_id)
#     db.add(user_trip_purpose)
#     db.commit()
#     return {"ok": True}


@router.post("/trip_purposes/{purpose_id}", tags=["trip_purposes"])
async def add_user_trip_purpose(
    purpose_id: int, user: user_dependency, db: db_dependency
):
    user_trip_purpose = models.UsersTripPurposes(user_id=user.id, purpose_id=purpose_id)
    db.add(user_trip_purpose)
    db.commit()
    return {"ok": True}


@router.patch("/trip_purposes/edit", tags=["trip_purposes"])
async def edit_trip_purposes(
    user: user_dependency, edit: schema.TagsEdit, db: db_dependency
):
    if not user:
        raise HTTPException(status_code=404, detail="Not authorized")
    db.execute(
        delete(models.UsersTripPurposes).where(
            models.UsersTripPurposes.user_id == user.id
        )
    )
    db.execute(
        insert(models.UsersTripPurposes).values(
            [{"user_id": user.id, "purpose_id": purpose_id} for purpose_id in edit.tags]
        )
    )
    db.commit()
    return {"ok": True}


@router.get("/trip_purposes", tags=["trip_purposes"])
async def get_user_trip_purposes(user: user_dependency, db: db_dependency):
    if not user:
        raise HTTPException(status_code=401, detail="Not authorized")
    result = (
        db.query(models.UsersTripPurposes)
        .filter(models.UsersTripPurposes.user_id == user.id)
        .all()
    )
    if not result:
        raise HTTPException(status_code=404, detail="No trip purposes found")
    return result


@router.delete("/trip_purposes/{purpose_id}", tags=["trip_purposes"])
async def delete_user_trip_purpose(
    user: user_dependency, purpose_id: int, db: db_dependency
):
    if not user:
        raise HTTPException(status_code=401, detail="Not authorized")
    user_trip_purpose = db.get(models.UsersTripPurposes, (user.id, purpose_id))
    if not user_trip_purpose:
        raise HTTPException(status_code=404, detail="Purpose not found")
    db.delete(user_trip_purpose)
    db.commit()
    return {"ok": True}


### departures


@router.get("/departures", tags=["departures"])
async def get_user_deapartures(user: user_dependency, db: db_dependency):
    if not user:
        raise HTTPException(status_code=401, detail="Not authorized")
    result = (
        db.query(models.UsersDepartures)
        .filter(models.UsersDepartures.user_id == user.id)
        .all()
    )
    if not result:
        raise HTTPException(status_code=404, detail="No locations found")
    return result


@router.post("/departures", tags=["departures"])
async def add_user_departure(object: schema.PivotTableBase, db: db_dependency):
    object = models.UsersDepartures(user_id=object.user_id, id=object.id)
    db.add(models)
    db.commit()
    return {"ok": True}


@router.patch("/departures/edit", tags=["departures"])
async def edit_user_departures(
    edit: schema.LocationsEdit, user: user_dependency, db: db_dependency
):
    if not user:
        raise HTTPException(status_code=404, detail="Not authorized")
    db.execute(
        delete(models.UsersDepartures).where(models.UsersDepartures.user_id == user.id)
    )
    db.execute(
        insert(models.UsersDepartures).values(
            [
                {"user_id": user.id, "location_id": location_id}
                for location_id in edit.locations
            ]
        )
    )
    db.commit()
    return {"ok": True}


# @router.delete("/departures/{user_id}/{departure_id}")
# async def delete_user_departure(user_id: UUID, departure_id: int, db: db_dependency):
#     user_departure = db.get(models.UsersArrivals, (user_id, departure_id))
#     if not user_departure:
#         raise HTTPException(status_code=404, detail="User not found")
#     db.delete(user_departure)
#     db.commit()
#     return {"ok": True}


### arrivals


@router.get("/arrivals", tags=["arrivals"])
async def get_user_arrivals(user: user_dependency, db: db_dependency):
    if not user:
        raise HTTPException(status_code=401, detail="Not authorized")
    result = (
        db.query(models.UsersArrivals)
        .filter(models.UsersArrivals.user_id == user.id)
        .all()
    )
    if not result:
        raise HTTPException(status_code=404, detail="No departures found")
    return result


@router.post("/arrivals", tags=["arrivals"])
async def add_user_arrival(object: schema.PivotTableBase, db: db_dependency):
    object = models.UsersArrivals(user_id=object.user_id, id=object.id)
    db.add(models)
    db.commit()
    return {"ok": True}


@router.patch("/arrivals/edit", tags=["arrivals"])
async def edit_user_arrivals(
    edit: schema.LocationsEdit, user: user_dependency, db: db_dependency
):
    if not user:
        raise HTTPException(status_code=404, detail="Not authorized")
    db.execute(
        delete(models.UsersArrivals).where(models.UsersArrivals.user_id == user.id)
    )
    db.execute(
        insert(models.UsersArrivals).values(
            [
                {"user_id": user.id, "location_id": location_id}
                for location_id in edit.locations
            ]
        )
    )
    db.commit()
    return {"ok": True}
