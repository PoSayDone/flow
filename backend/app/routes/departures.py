from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models, schema
from app.database import SessionLocal


router = APIRouter(prefix="/departures", tags=["departures"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


@router.post("")
async def add_departure(departure: schema.InfoTableBase, db: db_dependency):
    departure = models.Departures(
        departure_name=departure.name,
    )
    db.add(departure)
    db.commit()
    return {"ok": True}


@router.get("")
async def get_departures(db: db_dependency):
    result = db.query(models.Departures).all()
    if not result:
        raise HTTPException(status_code=404, detail="No departures found")
    return result


@router.delete("/{location_id}")
async def delete_departure(departure_id: int, db: db_dependency):
    departure = db.get(models.Departures, departure_id)
    if not departure:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(departure)
    db.commit()
    return {"ok": True}
