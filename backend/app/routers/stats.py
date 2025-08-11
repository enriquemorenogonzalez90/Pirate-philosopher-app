from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..database import get_session
from ..models import Author, School, Book, Quote
import random

router = APIRouter()

@router.get("/stats")
def get_stats(session: Session = Depends(get_session)):
    """Obtiene estadísticas generales de la biblioteca"""
    stats = {
        "authors": session.query(func.count(Author.id)).scalar(),
        "schools": session.query(func.count(School.id)).scalar(),
        "books": session.query(func.count(Book.id)).scalar(),
        "quotes": session.query(func.count(Quote.id)).scalar(),
    }
    return stats

@router.get("/random-quotes")
def get_random_quotes(limit: int = 3, session: Session = Depends(get_session)):
    """Obtiene citas aleatorias que cambian cada vez"""
    # Obtener todas las citas
    all_quotes = session.query(Quote).all()
    
    # Seleccionar aleatoriamente
    if len(all_quotes) <= limit:
        selected_quotes = all_quotes
    else:
        selected_quotes = random.sample(all_quotes, limit)
    
    # Convertir a formato de respuesta
    result = []
    for quote in selected_quotes:
        result.append({
            "id": quote.id,
            "texto": quote.texto,
            "autor_id": quote.autor_id
        })
    
    return result


