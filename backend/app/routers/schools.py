from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, selectinload
from sqlalchemy import select

from ..models.database import get_db
from ..models.models import School, Author
from ..models.schemas import SchoolCreate, SchoolRead, SchoolReadWithRelations, AuthorRead


router = APIRouter(prefix="/schools", tags=["schools"])


@router.get("/", response_model=List[SchoolRead])
def list_schools(
    q: Optional[str] = Query(default=None, description="Buscar por nombre"),
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    sort: Optional[str] = Query(default=None, description="nombre,-nombre,id,-id"),
    session: Session = Depends(get_db),
) -> List[SchoolRead]:
    stmt = select(School)
    if q:
        stmt = stmt.where(School.nombre.ilike(f"%{q}%"))
    if sort:
        mapping = {
            "nombre": School.nombre.asc(),
            "-nombre": School.nombre.desc(),
            "id": School.id.asc(),
            "-id": School.id.desc(),
        }
        order_by = mapping.get(sort)
        if order_by is not None:
            stmt = stmt.order_by(order_by)
    stmt = stmt.limit(limit).offset(offset)
    schools = session.execute(stmt).scalars().all()
    return schools


@router.get("/{school_id}", response_model=SchoolReadWithRelations)
def get_school(school_id: int, session: Session = Depends(get_db)) -> SchoolReadWithRelations:
    school = session.execute(
        select(School).options(selectinload(School.authors)).where(School.id == school_id)
    ).scalars().first()
    if not school:
        raise HTTPException(status_code=404, detail="Escuela no encontrada")
    return school


@router.post("/", response_model=SchoolRead, status_code=201)
def create_school(payload: SchoolCreate, session: Session = Depends(get_db)) -> SchoolRead:
    # Creamos la entidad a mano; Pydantic v2 usa model_dump
    school = School(**payload.model_dump())
    session.add(school)
    session.commit()
    session.refresh(school)
    return school


@router.put("/{school_id}", response_model=SchoolRead)
def update_school(school_id: int, payload: SchoolCreate, session: Session = Depends(get_db)) -> SchoolRead:
    school = session.get(School, school_id)
    if not school:
        raise HTTPException(status_code=404, detail="Escuela no encontrada")
    for key, value in payload.model_dump().items():
        setattr(school, key, value)
    session.add(school)
    session.commit()
    session.refresh(school)
    return school


@router.delete("/{school_id}", status_code=204)
def delete_school(school_id: int, session: Session = Depends(get_db)) -> None:
    school = session.get(School, school_id)
    if not school:
        raise HTTPException(status_code=404, detail="Escuela no encontrada")
    session.delete(school)
    session.commit()
    return None


@router.get("/{school_id}/authors", response_model=List[AuthorRead])
def list_school_authors(school_id: int, session: Session = Depends(get_db)) -> List[AuthorRead]:
    school = session.execute(
        select(School).options(selectinload(School.authors)).where(School.id == school_id)
    ).scalars().first()
    if not school:
        raise HTTPException(status_code=404, detail="Escuela no encontrada")
    return school.authors


