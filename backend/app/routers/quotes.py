from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, selectinload
from sqlalchemy import select

from ..database import get_session
from ..models import Quote
from ..schemas import QuoteCreate, QuoteRead, QuoteWithAuthor


router = APIRouter(prefix="/quotes", tags=["quotes"])


@router.get("/", response_model=List[QuoteWithAuthor])
def list_quotes(
    autor_id: Optional[int] = Query(default=None),
    q: Optional[str] = Query(default=None, description="Buscar por texto"),
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    session: Session = Depends(get_session),
) -> List[QuoteWithAuthor]:
    stmt = select(Quote).options(selectinload(Quote.author))
    if autor_id:
        stmt = stmt.where(Quote.autor_id == autor_id)
    if q:
        stmt = stmt.where(Quote.texto.ilike(f"%{q}%"))
    stmt = stmt.limit(limit).offset(offset)
    quotes = session.execute(stmt).scalars().all()
    return quotes


@router.get("/{quote_id}", response_model=QuoteRead)
def get_quote(quote_id: int, session: Session = Depends(get_session)) -> QuoteRead:
    quote = session.get(Quote, quote_id)
    if not quote:
        raise HTTPException(status_code=404, detail="Cita no encontrada")
    return quote


@router.post("/", response_model=QuoteRead, status_code=201)
def create_quote(payload: QuoteCreate, session: Session = Depends(get_session)) -> QuoteRead:
    quote = Quote(**payload.model_dump())
    session.add(quote)
    session.commit()
    session.refresh(quote)
    return quote


@router.put("/{quote_id}", response_model=QuoteRead)
def update_quote(quote_id: int, payload: QuoteCreate, session: Session = Depends(get_session)) -> QuoteRead:
    quote = session.get(Quote, quote_id)
    if not quote:
        raise HTTPException(status_code=404, detail="Cita no encontrada")
    for key, value in payload.model_dump().items():
        setattr(quote, key, value)
    session.add(quote)
    session.commit()
    session.refresh(quote)
    return quote


@router.delete("/{quote_id}", status_code=204)
def delete_quote(quote_id: int, session: Session = Depends(get_session)) -> None:
    quote = session.get(Quote, quote_id)
    if not quote:
        raise HTTPException(status_code=404, detail="Cita no encontrada")
    session.delete(quote)
    session.commit()
    return None


