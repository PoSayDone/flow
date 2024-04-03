from fastapi import APIRouter, HTTPException

from app import models, schema
from app.dependencies import db_dependency

router = APIRouter(prefix="/interests", tags=["interests"])


@router.post("")
async def add_interest(interest: schema.InfoTableBase, db: db_dependency):
    interest = models.Interests(
        interest_name=interest.name,
    )
    db.add(interest)
    db.commit()
    return {"ok": True}


@router.get("")
async def get_interests(db: db_dependency):
    result = db.query(models.Interests).all()
    if not result:
        raise HTTPException(status_code=404, detail="No interests found")
    return result


@router.delete("/{interest_id}")
async def delete_interest(interest_id: int, db: db_dependency):
    interest = db.get(models.Interests, interest_id)
    if not interest:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(interest)
    db.commit()
    return {"ok": True}
