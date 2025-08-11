from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, selectinload
from sqlalchemy import select

from ..database import get_session
from ..models import Book
from ..schemas import BookCreate, BookRead, BookWithAuthor


router = APIRouter(prefix="/books", tags=["books"])


@router.get("/", response_model=List[BookWithAuthor])
def list_books(
    autor_id: Optional[int] = Query(default=None),
    q: Optional[str] = Query(default=None, description="Buscar por título"),
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    session: Session = Depends(get_session),
) -> List[BookWithAuthor]:
    stmt = select(Book).options(selectinload(Book.author))
    if autor_id:
        stmt = stmt.where(Book.autor_id == autor_id)
    if q:
        stmt = stmt.where(Book.titulo.ilike(f"%{q}%"))
    stmt = stmt.limit(limit).offset(offset)
    books = session.execute(stmt).scalars().all()
    return books


@router.get("/{book_id}", response_model=BookRead)
def get_book(book_id: int, session: Session = Depends(get_session)) -> BookRead:
    book = session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    return book


@router.post("/", response_model=BookRead, status_code=201)
def create_book(payload: BookCreate, session: Session = Depends(get_session)) -> BookRead:
    book = Book(**payload.model_dump())
    session.add(book)
    session.commit()
    session.refresh(book)
    return book


@router.put("/{book_id}", response_model=BookRead)
def update_book(book_id: int, payload: BookCreate, session: Session = Depends(get_session)) -> BookRead:
    book = session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    for key, value in payload.model_dump().items():
        setattr(book, key, value)
    session.add(book)
    session.commit()
    session.refresh(book)
    return book


@router.delete("/{book_id}", status_code=204)
def delete_book(book_id: int, session: Session = Depends(get_session)) -> None:
    book = session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    session.delete(book)
    session.commit()
    return None


