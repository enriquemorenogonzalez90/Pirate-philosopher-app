from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, selectinload
from sqlalchemy import select

from ..database import get_session
from ..models import Author, School, Book, Quote
from ..schemas import (
    AuthorCreate,
    AuthorRead,
    AuthorReadWithRelations,
    SchoolRead,
    BookRead,
    QuoteRead,
)


router = APIRouter(prefix="/authors", tags=["authors"])


@router.get("/", response_model=List[AuthorRead])
def list_authors(
    q: Optional[str] = Query(default=None, description="Buscar por nombre"),
    epoca: Optional[str] = Query(default=None),
    school_id: Optional[int] = Query(default=None),
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    sort: Optional[str] = Query(default=None, description="nombre,-nombre,id,-id"),
    session: Session = Depends(get_session),
) -> List[AuthorRead]:
    stmt = select(Author)
    if q:
        stmt = stmt.where(Author.nombre.ilike(f"%{q}%"))
    if epoca:
        stmt = stmt.where(Author.epoca == epoca)
    if school_id:
        stmt = stmt.join(Author.schools).where(School.id == school_id)

    if sort:
        mapping = {
            "nombre": Author.nombre.asc(),
            "-nombre": Author.nombre.desc(),
            "id": Author.id.asc(),
            "-id": Author.id.desc(),
        }
        order_by = mapping.get(sort)
        if order_by is not None:
            stmt = stmt.order_by(order_by)

    stmt = stmt.limit(limit).offset(offset)
    authors = session.execute(stmt).scalars().all()
    return authors


@router.get("/{author_id}", response_model=AuthorReadWithRelations)
def get_author(author_id: int, session: Session = Depends(get_session)) -> AuthorReadWithRelations:
    author = session.execute(
        select(Author)
        .options(selectinload(Author.schools), selectinload(Author.books))
        .where(Author.id == author_id)
    ).scalars().first()
    if not author:
        raise HTTPException(status_code=404, detail="Autor no encontrado")
    return author


@router.post("/", response_model=AuthorRead, status_code=201)
def create_author(payload: AuthorCreate, session: Session = Depends(get_session)) -> AuthorRead:
    author = Author(**payload.model_dump())
    session.add(author)
    session.commit()
    session.refresh(author)
    return author


@router.put("/{author_id}", response_model=AuthorRead)
def update_author(author_id: int, payload: AuthorCreate, session: Session = Depends(get_session)) -> AuthorRead:
    author = session.get(Author, author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Autor no encontrado")
    for key, value in payload.model_dump().items():
        setattr(author, key, value)
    session.add(author)
    session.commit()
    session.refresh(author)
    return author


@router.delete("/{author_id}", status_code=204)
def delete_author(author_id: int, session: Session = Depends(get_session)) -> None:
    author = session.get(Author, author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Autor no encontrado")
    session.delete(author)
    session.commit()
    return None


@router.get("/{author_id}/schools", response_model=List[SchoolRead])
def list_author_schools(author_id: int, session: Session = Depends(get_session)) -> List[SchoolRead]:
    author = session.execute(
        select(Author).options(selectinload(Author.schools)).where(Author.id == author_id)
    ).scalars().first()
    if not author:
        raise HTTPException(status_code=404, detail="Autor no encontrado")
    return author.schools


@router.post("/{author_id}/schools/{school_id}", status_code=204)
def link_author_school(author_id: int, school_id: int, session: Session = Depends(get_session)) -> None:
    author = session.get(Author, author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Autor no encontrado")
    school = session.get(School, school_id)
    if not school:
        raise HTTPException(status_code=404, detail="Escuela no encontrada")
    if school not in author.schools:
        author.schools.append(school)
        session.add(author)
        session.commit()
    return None


@router.delete("/{author_id}/schools/{school_id}", status_code=204)
def unlink_author_school(author_id: int, school_id: int, session: Session = Depends(get_session)) -> None:
    author = session.get(Author, author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Autor no encontrado")
    school = session.get(School, school_id)
    if not school:
        raise HTTPException(status_code=404, detail="Escuela no encontrada")
    if school in author.schools:
        author.schools.remove(school)
        session.add(author)
        session.commit()
    return None


@router.get("/{author_id}/books", response_model=List[BookRead])
def list_author_books(author_id: int, session: Session = Depends(get_session)) -> List[BookRead]:
    books = session.execute(select(Book).where(Book.autor_id == author_id)).scalars().all()
    return books


@router.get("/{author_id}/quotes", response_model=List[QuoteRead])
def list_author_quotes(author_id: int, session: Session = Depends(get_session)) -> List[QuoteRead]:
    quotes = session.execute(select(Quote).where(Quote.autor_id == author_id)).scalars().all()
    return quotes


