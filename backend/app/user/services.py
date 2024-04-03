from sqlalchemy import schema
from sqlalchemy.orm import Session

from app import models


async def update_user_status(
    db: Session, user: models.Users, edit: schema.StatusDataEdit
):
    """
    Updates a user's interests based on a list of interest IDs.
    """

    # Clear existing user interests
    user.status = edit.status
    user.trip_purposes = []
    user.departures = []
    user.arrivals = []

    # Add new interests based on IDs
    for trip_purpose_id in edit.trip_purposes:
        interest = db.query(models.Interests).get(id)
        if interest:
            user.interests.append(interest)

    db.add(user)
    db.commit()
