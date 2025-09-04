"""
Books router for Firestore backend
"""
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query, Depends

from ..services.firestore_service import FirestoreService
from ..models.firestore_models import BookResponse


router = APIRouter(prefix="/books", tags=["books"])


def get_firestore_service() -> FirestoreService:
    """Dependency to get Firestore service"""
    return FirestoreService()


@router.get("/", response_model=List[BookResponse])
async def list_books(
    autor_id: Optional[str] = Query(default=None, description="Filter by author ID"),
    limit: int = Query(default=50, ge=1, le=100),
    offset: int = Query(default=0, ge=0, description="Number of books to skip"),
    q: Optional[str] = Query(default=None, description="Search in title and description"),
    service: FirestoreService = Depends(get_firestore_service)
):
    """Get list of books, optionally filtered by author and search term"""
    try:
        books = await service.get_books(limit=limit, offset=offset, autor_id=autor_id, search_query=q)
        return books
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching books: {str(e)}")


@router.get("/count")
async def count_books(
    autor_id: Optional[str] = Query(default=None, description="Filter by author ID"),
    q: Optional[str] = Query(default=None, description="Search in title and description"),
    service: FirestoreService = Depends(get_firestore_service)
):
    """Get total count of books with optional filters"""
    try:
        count = await service.count_books(autor_id=autor_id, search_query=q)
        return {"count": count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error counting books: {str(e)}")