from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models, schema
from app.database import SessionLocal


router = APIRouter(prefix="/role", tags=["roles"])

from app.dependencies import db_dependency


@router.post("/")
async def add_role(role: schema.InfoTableBase, db: db_dependency):
    role = models.Roles(
        role_name=role.name,
    )
    db.add(role)
    db.commit()
    return {"ok": True}


@router.get("/")
async def get_roles(db: db_dependency):
    result = db.query(models.Roles).all()
    if not result:
        raise HTTPException(status_code=404, detail="No roles found")
    return result


@router.delete("/{role_id}")
async def delete_role(role_id: int, db: db_dependency):
    role = db.get(models.Roles, role_id)
    if not role:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(role)
    db.commit()
    return {"ok": True}
