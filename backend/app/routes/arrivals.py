from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models, schema
from app.database import SessionLocal


router = APIRouter(prefix="/arrivals", tags=["arrivals"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


@router.post("")
async def add_arrival(location: schema.InfoTableBase, db: db_dependency):
    location = models.Arrivals(
        location_name=location.name,
    )
    db.add(location)
    db.commit()
    return {"ok": True}


@router.get("")
async def get_arrivals(db: db_dependency):
    result = db.query(models.Arrivals).all()
    if not result:
        raise HTTPException(status_code=404, detail="No locations found")
    return result


@router.delete("/{location_id}")
async def delete_arrival(arrival_id: int, db: db_dependency):
    arrival = db.get(models.Arrivals, arrival_id)
    if not arrival:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(arrival)
    db.commit()
    return {"ok": True}
