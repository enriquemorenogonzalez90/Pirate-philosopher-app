"""
Schools router for Firestore backend
"""
from typing import List
from fastapi import APIRouter, HTTPException, Query, Depends

from ..services.firestore_service import FirestoreService
from ..models.firestore_models import SchoolResponse


router = APIRouter(prefix="/schools", tags=["schools"])


def get_firestore_service() -> FirestoreService:
    """Dependency to get Firestore service"""
    return FirestoreService()


@router.get("/", response_model=List[SchoolResponse])
async def list_schools(
    limit: int = Query(default=50, ge=1, le=100),
    service: FirestoreService = Depends(get_firestore_service)
):
    """Get list of philosophical schools"""
    try:
        schools = await service.get_schools(limit=limit)
        return schools
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching schools: {str(e)}")


@router.get("/{school_id}", response_model=SchoolResponse)
async def get_school(
    school_id: str,
    service: FirestoreService = Depends(get_firestore_service)
):
    """Get school by ID"""
    try:
        school = await service.get_school(school_id)
        if not school:
            raise HTTPException(status_code=404, detail="School not found")
        return school
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching school: {str(e)}")