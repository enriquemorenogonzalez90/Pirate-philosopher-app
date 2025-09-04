"""
Firestore models and schemas for Filosofía App
"""
from datetime import datetime, timezone
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class AuthorModel(BaseModel):
    """Author model for Firestore"""
    # IDs
    external_id: Optional[str] = None
    
    # Basic info
    nombre: str
    username: Optional[str] = None
    vida: Optional[str] = None  # e.g., "1723-1790"
    descripcion_topica: Optional[str] = None
    areas_interes: Optional[str] = None
    
    # Detailed dates from API
    fecha_nacimiento_completa: Optional[str] = None  # "16 June 1723"
    fecha_muerte_completa: Optional[str] = None      # "17 July 1790"
    año_nacimiento: Optional[str] = None             # "1723 AD"
    año_muerte: Optional[str] = None                 # "1790 AD"
    
    # Location
    lugar_nacimiento: Optional[str] = None
    
    # Philosophy
    escuela_principal: Optional[str] = None
    school_ids: List[str] = Field(default_factory=list)  # Array of school document IDs
    
    # Links
    enlace_iep: Optional[str] = None        # Main biography
    enlace_stanford: Optional[str] = None   # SEP
    titulo_wiki: Optional[str] = None
    
    # Images (JSON with all variants)
    imagenes: Optional[Dict[str, Any]] = None
    imagen_url: Optional[str] = None  # Main image for compatibility
    
    # Books info
    tiene_libros: bool = False
    libros_librivox: Optional[Dict[str, Any]] = None
    
    # Biography
    biografia: Optional[str] = None
    
    # Metadata
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    class Config:
        arbitrary_types_allowed = True


class SchoolModel(BaseModel):
    """School model for Firestore"""
    nombre: str
    imagen_url: Optional[str] = None
    descripcion: Optional[str] = None
    
    # Arrays instead of relationships
    author_ids: List[str] = Field(default_factory=list)  # Array of author document IDs
    
    # Metadata
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    class Config:
        arbitrary_types_allowed = True


class BookModel(BaseModel):
    """Book model for Firestore"""
    # External IDs
    external_id: Optional[str] = None
    librivox_id: Optional[str] = None
    
    # Basic info
    titulo: str
    descripcion: Optional[str] = None
    
    # Images and links
    imagen_url: Optional[str] = None
    cover_art_path: Optional[str] = None  # From LibriVox
    librivox_url: Optional[str] = None
    
    # Book type
    es_audiolibro: bool = False
    es_ebook: bool = False
    
    # Author relationship (denormalized)
    autor_id: Optional[str] = None  # Author document ID
    autor_nombre: Optional[str] = None  # Denormalized for quick access
    
    # Metadata
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    class Config:
        arbitrary_types_allowed = True


class QuoteModel(BaseModel):
    """Quote model for Firestore"""
    # External IDs
    external_id: Optional[str] = None
    internal_id: Optional[str] = None
    
    # Quote content
    texto: str
    
    # Source info
    obra: Optional[str] = None
    año: Optional[str] = None
    
    # Author relationship (denormalized)
    autor_id: Optional[str] = None  # Author document ID
    autor_nombre: Optional[str] = None  # Denormalized for quick access
    philosopher_external_id: Optional[str] = None  # For API mapping
    
    # Metadata
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    class Config:
        arbitrary_types_allowed = True


# Response models for API
class AuthorResponse(AuthorModel):
    """Author response with computed fields"""
    id: str  # Firestore document ID
    books_count: int = 0
    quotes_count: int = 0


class SchoolResponse(SchoolModel):
    """School response with computed fields"""
    id: str  # Firestore document ID
    authors_count: int = 0


class BookResponse(BookModel):
    """Book response"""
    id: str  # Firestore document ID
    author: Optional[Dict[str, Any]] = None  # Author information for frontend compatibility


class QuoteResponse(QuoteModel):
    """Quote response"""
    id: str  # Firestore document ID


# Collection names
COLLECTIONS = {
    'authors': 'authors',
    'schools': 'schools', 
    'books': 'books',
    'quotes': 'quotes'
}