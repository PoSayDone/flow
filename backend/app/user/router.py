import io
from uuid import UUID
import uuid
from app.user.services import calculate_soulmate_score
from fastapi import APIRouter, File, HTTPException, UploadFile
from sqlalchemy import and_, insert, or_
from PIL import Image


from app import models, schema
from app.chat.services import create_conversation_db
from app.auth.services import user_dependency
from app.dependencies import db_dependency


user_router = APIRouter(prefix="/user", tags=["user"])


# @user_router.delete("/{user_id}")
# async def delete_user(user_id: UUID, db: db_dependency):
#     user = db.get(models.Users, user_id)
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")
#     db.delete(user)
#     db.commit()
#     return {"ok": True}


@user_router.patch("/")
async def update_user(
    user: user_dependency, user_update: schema.UserUpdate, db: db_dependency
):
    if not user:
        raise HTTPException(status_code=404, detail="Not authorized")
    for field, value in user_update.dict(exclude_unset=True).items():
        setattr(user, field, value)
    db.commit()
    return {"message": "User updated successfully"}


@user_router.patch("/image")
async def update_user_image(
    user: user_dependency, db: db_dependency, image: UploadFile = File(...)
):
    if not user:
        raise HTTPException(status_code=404, detail="Not authorized")
    extension = image.filename.split(".")[1]
    if extension not in ["png", "jpg", "JPG", "jpeg", "webp", "JPEG"]:
        raise HTTPException(status_code=422, detail="Wrong image format")
    filename = f"{uuid.uuid4()}.webp"
    contents = await image.read()
    result_image = Image.open(io.BytesIO(contents))
    result_image.thumbnail((1080, 1080), Image.Resampling.LANCZOS)
    result_image.save(f"images/{filename}", "webp", optimize=True, quality=80)
    user.user_image = filename
    db.add(user)
    db.commit()

    return {"message": "profile_picture updated"}


@user_router.get("/soulmates/{count}")
async def get_soulmates(count: int, db: db_dependency, user: user_dependency):
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    count = min(3, count)

    trace = get_or_set_feed_trace(user)

    subquery = (
        db.query(models.Matches.liked_user_id)
        .filter(models.Matches.user_id == user.id)
        .union(
            db.query(models.Matches.user_id).filter(
                models.Matches.liked_user_id == user.id, models.Matches.mutual == True
            )
        )
        .correlate(models.Users)
        .scalar_subquery()
    )

    filtered_users = (
        db.query(models.Users)
        .filter(models.Users.id != user.id, ~models.Users.id.in_(subquery))
        .all()
    )

    # FIXME это типо костыль, но я хз как по другому, потому что фильтр
    # не переваривает trace.contains_user

    filtered_users = filter(lambda u: not trace.contains_user(u), filtered_users)

    # Define matching criteria and calculate scores for each user
    soulmate_scores = {}
    for scoring_user in filtered_users:
        score = calculate_soulmate_score(db, user, scoring_user)
        soulmate_scores[scoring_user] = score

    # Sort users by score and return top 'count' soulmates
    sorted_users = sorted(soulmate_scores.items(), key=lambda x: x[1], reverse=True)

    top_soulmates = [u for u, _ in sorted_users[:count]]

    result = schema.SoulmatesResponse.model_validate({"soulmates": top_soulmates})

    return result


### status_data


@user_router.patch("/status_data/edit", tags=["status"])
async def edit_user_status_data(
    user: user_dependency,
    db: db_dependency,
    edit: schema.StatusDataEdit,
):
    if not user:
        raise HTTPException(status_code=404, detail="Not authorized")
    if not user:
        raise HTTPException(status_code=404, detail="Not authorized")

    user.status = edit.user_status
    if len(edit.user_trip_purposes) > 0:
        user.trip_purposes = []
    if len(edit.user_departures) > 0:
        user.departures = []
    if len(edit.user_arrivals) > 0:
        user.arrivals = []
    db.commit()

    if len(edit.user_trip_purposes) > 0:
        db.execute(
            insert(models.user_trip_purpose_table).values(
                [
                    {"user_id": user.id, "trip_purpose_id": id}
                    for id in edit.user_trip_purposes
                ]
            )
        )
    if len(edit.user_departures) > 0:
        db.execute(
            insert(models.user_departure_table).values(
                [
                    {"user_id": user.id, "departure_id": id}
                    for id in edit.user_departures
                ]
            )
        )
    if len(edit.user_arrivals) > 0:
        db.execute(
            insert(models.user_arrival_table).values(
                [{"user_id": user.id, "arrival_id": id} for id in edit.user_arrivals]
            )
        )
    db.commit()


### profile


@user_router.get("/profile")
async def get_profile(user: user_dependency):
    if not user:
        raise HTTPException(status_code=401, detail="Not authorized")
    result = schema.Profile.model_validate(user)
    return result


@user_router.get("/profile/{user_id}")
async def get_profile_w_id(user_id: UUID, db: db_dependency):
    user_db = db.get(models.Users, user_id)
    if not user_db:
        raise HTTPException(status_code=404, detail="User not found")
    result = schema.Profile.model_validate(user_db)
    return result


# ### roles
#
#
# @user_router.get("/roles")
# async def get_users_roles(db: db_dependency):
#     result = db.query(models.UsersRoles).all()
#     if not result:
#         raise HTTPException(status_code=404, detail="No roles found")
#     return result
#
#
# @user_router.post("/roles")
# async def add_user_role(object: schema.PivotTableBase, db: db_dependency):
#     object = models.UsersRoles(user_id=object.user_id, id=object.id)
#     db.add(models)
#     db.commit()
#     return {"ok": True}
#
#
# @user_router.delete("/roles/{user_id}/{role_id}")
# async def delete_user_role(user_id: UUID, role_id: int, db: db_dependency):
#     user_role = db.get(models.UsersRoles, (user_id, role_id))
#     if not user_role:
#         raise HTTPException(status_code=404, detail="User not found")
#     db.delete(user_role)
#     db.commit()
#     return {"ok": True}


### matches


class UserTrace:
    def __init__(self, user_id) -> None:
        self.user_id = user_id
        self.traced_users = set()

    def add_traced_user(self, user: models.Users):
        self.traced_users.add(user.id)

    def contains_user(self, user: models.Users) -> bool:
        contains = user.id in self.traced_users
        return contains

    def __str__(self):
        return f"FeedTrace(userId={self.user_id}, tracedUsers={self.traced_users})"


in_memory_feed_trace = {}


def get_or_set_feed_trace(user: models.Users) -> UserTrace:
    user_trace = in_memory_feed_trace.get(user.id)

    if not user_trace:
        user_trace = UserTrace(user_id=user.id)
        in_memory_feed_trace[user.id] = user_trace

    return user_trace


@user_router.post("/dislike/{liked_user_id}", tags=["matches"])
async def add_dislike(liked_user_id: UUID, user: user_dependency, db: db_dependency):
    if not user:
        raise HTTPException(status_code=401, detail="Not authorized")

    recepient = db.get(models.Users, liked_user_id)

    if not recepient:
        raise HTTPException(status_code=404, detail="Recepient not found")

    return {"ok": True}


@user_router.post("/like/{liked_user_id}", tags=["matches"])
async def add_like(liked_user_id: UUID, user: user_dependency, db: db_dependency):
    if not user:
        raise HTTPException(status_code=401, detail="Not authorized")

    recepient = db.get(models.Users, liked_user_id)

    if not recepient:
        raise HTTPException(status_code=404, detail="Recepient not found")

    user_trace = get_or_set_feed_trace(user)
    user_trace.add_traced_user(recepient)

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

    if existing_match and existing_match.user_id != user.id:
        existing_match.mutual = True
        await create_conversation_db(db, user, recepient)
    else:
        match = models.Matches(user_id=user.id, liked_user_id=liked_user_id)
        db.add(match)
    db.commit()

    return {"ok": True}


@user_router.get("/matches", tags=["matches"])
async def get_matches(db: db_dependency):
    result = db.query(models.Matches).all()
    if not result:
        raise HTTPException(status_code=404, detail="No locations found")
    return result


### interests


# # @router.post("/interests/{user_id}/{interest_id}")
# # async def add_user_interest_by_id(user_id: UUID, interest_id: int, db: db_dependency):
# #     user_interest = models.UsersInterests(user_id=user_id, interest_id=interest_id)
# #     db.add(user_interest)
# #     db.commit()
# #     return {"ok": True}
#
#
# @user_router.get("/interests", tags=["interests"])
# async def get_user_interests(user: user_dependency, db: db_dependency):
#     if not user:
#         raise HTTPException(status_code=401, detail="Not authorized")
#     result = (
#         db.query(models.UsersInterests)
#         .filter(models.UsersInterests.user_id == user.di)
#         .all()
#     )
#     if not result:
#         raise HTTPException(status_code=404, detail="No interests found")
#     return result
#
#
# @user_router.post("/interests/{interest_id}", tags=["interests"])
# async def add_user_interest(interest_id: int, user: user_dependency, db: db_dependency):
#     user_interest = models.UsersInterests(user_id=user.id, interest_id=interest_id)
#     db.add(user_interest)
#     db.commit()
#     return {"ok": True}
#
#
@user_router.patch("/interests/edit", tags=["interests"])
async def edit_user_interests(
    user: user_dependency, edit: schema.TagsEdit, db: db_dependency
):
    if not user:
        raise HTTPException(status_code=404, detail="Not authorized")
    user.interests = []
    db.commit()
    db.execute(
        insert(models.user_interest_table).values(
            [
                {"user_id": user.id, "interest_id": interest_id}
                for interest_id in edit.tags
            ]
        )
    )
    db.commit()
    return {"ok": True}


#
#
# @user_router.delete("/interests/{interest_id}", tags=["interests"])
# async def delete_user_interest(
#     user: user_dependency, interest_id: int, db: db_dependency
# ):
#     if not user:
#         raise HTTPException(status_code=401, detail="Not authorized")
#     user_interest = db.get(models.UsersInterests, (user.id, interest_id))
#     if not user_interest:
#         raise HTTPException(status_code=404, detail="Interest not found")
#     db.delete(user_interest)
#     db.commit()
#     return {"ok": True}
#
#
# ### trip purposes
#
#
# # @router.post("/trip_purposes/{user_id}/{purpose_id}")
# # async def add_user_trip_purpose_by_id(
# #     purpose_id: int, user_id: UUID, db: db_dependency
# # ):
# #     user_trip_purpose = models.UsersTripPurposes(user_id=user_id, purpose_id=purpose_id)
# #     db.add(user_trip_purpose)
# #     db.commit()
# #     return {"ok": True}
#
#
# @user_router.post("/trip_purposes/{purpose_id}", tags=["trip_purposes"])
# async def add_user_trip_purpose(
#     purpose_id: int, user: user_dependency, db: db_dependency
# ):
#     user_trip_purpose = models.UsersTripPurposes(user_id=user.id, purpose_id=purpose_id)
#     db.add(user_trip_purpose)
#     db.commit()
#     return {"ok": True}
#
#
# @user_router.patch("/trip_purposes/edit", tags=["trip_purposes"])
# async def edit_trip_purposes(
#     user: user_dependency, edit: schema.TagsEdit, db: db_dependency
# ):
#     if not user:
#         raise HTTPException(status_code=404, detail="Not authorized")
#     db.execute(
#         delete(models.UsersTripPurposes).where(
#             models.UsersTripPurposes.user_id == user.id
#         )
#     )
#     db.execute(
#         insert(models.UsersTripPurposes).values(
#             [{"user_id": user.id, "purpose_id": purpose_id} for purpose_id in edit.tags]
#         )
#     )
#     db.commit()
#     return {"ok": True}
#
#
# @user_router.get("/trip_purposes", tags=["trip_purposes"])
# async def get_user_trip_purposes(user: user_dependency, db: db_dependency):
#     if not user:
#         raise HTTPException(status_code=401, detail="Not authorized")
#     result = (
#         db.query(models.UsersTripPurposes)
#         .filter(models.UsersTripPurposes.user_id == user.id)
#         .all()
#     )
#     if not result:
#         raise HTTPException(status_code=404, detail="No trip purposes found")
#     return result
#
#
# @user_router.delete("/trip_purposes/{purpose_id}", tags=["trip_purposes"])
# async def delete_user_trip_purpose(
#     user: user_dependency, purpose_id: int, db: db_dependency
# ):
#     if not user:
#         raise HTTPException(status_code=401, detail="Not authorized")
#     user_trip_purpose = db.get(models.UsersTripPurposes, (user.id, purpose_id))
#     if not user_trip_purpose:
#         raise HTTPException(status_code=404, detail="Purpose not found")
#     db.delete(user_trip_purpose)
#     db.commit()
#     return {"ok": True}
#
#
# ### departures
#
#
# @user_router.get("/departures", tags=["departures"])
# async def get_user_deapartures(user: user_dependency, db: db_dependency):
#     if not user:
#         raise HTTPException(status_code=401, detail="Not authorized")
#     result = (
#         db.query(models.UsersDepartures)
#         .filter(models.UsersDepartures.user_id == user.id)
#         .all()
#     )
#     if not result:
#         raise HTTPException(status_code=404, detail="No locations found")
#     return result
#
#
# @user_router.post("/departures", tags=["departures"])
# async def add_user_departure(object: schema.PivotTableBase, db: db_dependency):
#     object = models.UsersDepartures(user_id=object.user_id, id=object.id)
#     db.add(models)
#     db.commit()
#     return {"ok": True}
#
#
# @user_router.patch("/departures/edit", tags=["departures"])
# async def edit_user_departures(
#     edit: schema.LocationsEdit, user: user_dependency, db: db_dependency
# ):
#     if not user:
#         raise HTTPException(status_code=404, detail="Not authorized")
#     db.execute(
#         delete(models.UsersDepartures).where(models.UsersDepartures.user_id == user.id)
#     )
#     db.execute(
#         insert(models.UsersDepartures).values(
#             [
#                 {"user_id": user.id, "location_id": location_id}
#                 for location_id in edit.locations
#             ]
#         )
#     )
#     db.commit()
#     return {"ok": True}
#
#
# # @router.delete("/departures/{user_id}/{departure_id}")
# # async def delete_user_departure(user_id: UUID, departure_id: int, db: db_dependency):
# #     user_departure = db.get(models.UsersArrivals, (user_id, departure_id))
# #     if not user_departure:
# #         raise HTTPException(status_code=404, detail="User not found")
# #     db.delete(user_departure)
# #     db.commit()
# #     return {"ok": True}
#
#
# ### arrivals
#
#
# @user_router.get("/arrivals", tags=["arrivals"])
# async def get_user_arrivals(user: user_dependency, db: db_dependency):
#     if not user:
#         raise HTTPException(status_code=401, detail="Not authorized")
#     result = (
#         db.query(models.UsersArrivals)
#         .filter(models.UsersArrivals.user_id == user.id)
#         .all()
#     )
#     if not result:
#         raise HTTPException(status_code=404, detail="No departures found")
#     return result
#
#
# @user_router.post("/arrivals", tags=["arrivals"])
# async def add_user_arrival(object: schema.PivotTableBase, db: db_dependency):
#     object = models.UsersArrivals(user_id=object.user_id, id=object.id)
#     db.add(models)
#     db.commit()
#     return {"ok": True}
#
#
# @user_router.patch("/arrivals/edit", tags=["arrivals"])
# async def edit_user_arrivals(
#     edit: schema.LocationsEdit, user: user_dependency, db: db_dependency
# ):
#     if not user:
#         raise HTTPException(status_code=404, detail="Not authorized")
#     db.execute(
#         delete(models.UsersArrivals).where(models.UsersArrivals.user_id == user.id)
#     )
#     db.execute(
#         insert(models.UsersArrivals).values(
#             [
#                 {"user_id": user.id, "location_id": location_id}
#                 for location_id in edit.locations
#             ]
#         )
#     )
#     db.commit()
#     return {"ok": True}
