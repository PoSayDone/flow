from typing import Annotated
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models, schema
from app.database import SessionLocal
from app.routes import auth


router = APIRouter(prefix="/trip_purposes", tags=["trip_purposes"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


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
