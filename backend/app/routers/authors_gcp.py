"""
Authors router for Firestore backend
"""
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query, Depends

from ..services.firestore_service import FirestoreService
from ..models.firestore_models import AuthorResponse, BookResponse, QuoteResponse


router = APIRouter(prefix="/authors", tags=["authors"])


def get_firestore_service() -> FirestoreService:
    """Dependency to get Firestore service"""
    return FirestoreService()


@router.get("/", response_model=List[AuthorResponse])
async def list_authors(
    q: Optional[str] = Query(default=None, description="Search by name"),
    limit: int = Query(default=50, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    service: FirestoreService = Depends(get_firestore_service)
):
    """Get paginated list of authors"""
    try:
        if q:
            # Search by name
            authors = await service.search_authors(query=q, limit=limit)
        else:
            # Regular pagination
            authors = await service.get_authors(limit=limit, offset=offset)
        
        return authors
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching authors: {str(e)}")


@router.get("/{author_id}", response_model=AuthorResponse)
async def get_author(
    author_id: str,
    service: FirestoreService = Depends(get_firestore_service)
):
    """Get author by ID"""
    try:
        author = await service.get_author(author_id)
        if not author:
            raise HTTPException(status_code=404, detail="Author not found")
        return author
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching author: {str(e)}")


@router.get("/{author_id}/books", response_model=List[BookResponse])
async def get_author_books(
    author_id: str,
    limit: int = Query(default=50, ge=1, le=100),
    service: FirestoreService = Depends(get_firestore_service)
):
    """Get books by author"""
    try:
        # First check if author exists
        author = await service.get_author(author_id)
        if not author:
            raise HTTPException(status_code=404, detail="Author not found")
        
        # Get books by author
        books = await service.get_books(limit=limit, autor_id=author_id)
        return books
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching author books: {str(e)}")


@router.get("/{author_id}/quotes", response_model=List[QuoteResponse])
async def get_author_quotes(
    author_id: str,
    limit: int = Query(default=50, ge=1, le=100),
    service: FirestoreService = Depends(get_firestore_service)
):
    """Get quotes by author"""
    try:
        # First check if author exists
        author = await service.get_author(author_id)
        if not author:
            raise HTTPException(status_code=404, detail="Author not found")
        
        # Get quotes by author
        quotes = await service.get_quotes(limit=limit, autor_id=author_id)
        return quotes
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching author quotes: {str(e)}")