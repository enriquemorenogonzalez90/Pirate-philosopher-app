"""
Stats router for Firestore backend
"""
from typing import Dict, Any
from fastapi import APIRouter, HTTPException, Depends

from ..services.firestore_service import FirestoreService


router = APIRouter(prefix="/stats", tags=["stats"])


def get_firestore_service() -> FirestoreService:
    """Dependency to get Firestore service"""
    return FirestoreService()


@router.get("/", response_model=Dict[str, Any])
async def get_stats(
    service: FirestoreService = Depends(get_firestore_service)
):
    """Get application statistics"""
    try:
        stats = await service.get_stats()
        return {
            "total_authors": stats.get("authors_count", 0),
            "total_schools": stats.get("schools_count", 0),
            "total_books": stats.get("books_count", 0),
            "total_quotes": stats.get("quotes_count", 0),
            "database": "firestore",
            "platform": "gcp-cloud-functions"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching stats: {str(e)}")