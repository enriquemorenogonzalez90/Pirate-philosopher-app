from __future__ import annotations

from datetime import date
from typing import Optional, List

from pydantic import BaseModel, ConfigDict, Field


class ORMModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class AuthorBase(ORMModel):
    nombre: str
    epoca: Optional[str] = None
    fecha_nacimiento: Optional[date] = None
    fecha_defuncion: Optional[date] = None
    imagen_url: Optional[str] = None
    biografia: Optional[str] = None
    escuela_pensamiento: Optional[str] = None
    areas_interes: Optional[str] = None
    enlace_iep: Optional[str] = None
    enlace_stanford: Optional[str] = None


class AuthorCreate(AuthorBase):
    pass


class AuthorRead(AuthorBase):
    id: int


class SchoolBase(ORMModel):
    nombre: str
    imagen_url: Optional[str] = None
    descripcion: Optional[str] = None


class SchoolCreate(SchoolBase):
    pass


class SchoolRead(SchoolBase):
    id: int


class BookBase(ORMModel):
    titulo: str
    imagen_url: Optional[str] = None
    descripcion: Optional[str] = None


class BookCreate(BookBase):
    autor_id: int


class BookRead(BookBase):
    id: int
    autor_id: int


class BookWithAuthor(BookBase):
    id: int
    autor_id: int
    author: AuthorBase


class QuoteBase(ORMModel):
    texto: str


class QuoteCreate(QuoteBase):
    autor_id: int


class QuoteRead(QuoteBase):
    id: int
    autor_id: Optional[int] = None


class QuoteWithAuthor(QuoteBase):
    id: int
    autor_id: Optional[int] = None
    author: Optional[AuthorBase] = None


class AuthorReadWithRelations(AuthorRead):
    schools: List[SchoolRead] = Field(default_factory=list)
    books: List[BookRead] = Field(default_factory=list)


class SchoolReadWithRelations(SchoolRead):
    authors: List[AuthorRead] = Field(default_factory=list)


