"""
Quotes router for Firestore backend
"""
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query, Depends

from ..services.firestore_service import FirestoreService
from ..models.firestore_models import QuoteResponse


router = APIRouter(prefix="/quotes", tags=["quotes"])


def get_firestore_service() -> FirestoreService:
    """Dependency to get Firestore service"""
    return FirestoreService()


@router.get("/", response_model=List[QuoteResponse])
async def list_quotes(
    autor_id: Optional[str] = Query(default=None, description="Filter by author ID"),
    limit: int = Query(default=50, ge=1, le=100),
    service: FirestoreService = Depends(get_firestore_service)
):
    """Get list of quotes, optionally filtered by author"""
    try:
        quotes = await service.get_quotes(limit=limit, autor_id=autor_id)
        return quotes
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching quotes: {str(e)}")


@router.get("/random", response_model=QuoteResponse)
async def get_random_quote(
    service: FirestoreService = Depends(get_firestore_service)
):
    """Get a random quote"""
    try:
        quote = await service.get_random_quote()
        if not quote:
            raise HTTPException(status_code=404, detail="No quotes available")
        return quote
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching random quote: {str(e)}")