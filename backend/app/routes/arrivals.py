from fastapi import APIRouter, HTTPException

from app import models, schema
from app.dependencies import db_dependency


router = APIRouter(prefix="/arrivals", tags=["arrivals"])


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
