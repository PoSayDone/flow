from fastapi import APIRouter, HTTPException

from app import models, schema
from app.dependencies import db_dependency

router = APIRouter(prefix="/trip_purposes", tags=["trip_purposes"])


@router.post("")
async def add_trip_purpose(purpose: schema.InfoTableBase, db: db_dependency):
    purpose = models.TripPurposes(
        purpose_name=purpose.name,
    )
    db.add(purpose)
    db.commit()
    return {"ok": True}


@router.get("")
async def get_trip_purposes(db: db_dependency):
    result = db.query(models.TripPurposes).all()
    if not result:
        raise HTTPException(status_code=404, detail="No trip purposes found")
    return result
