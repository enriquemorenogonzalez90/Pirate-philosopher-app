from __future__ import annotations

from datetime import date
from typing import Optional, List

from sqlalchemy import String, Integer, ForeignKey, Table, Column, Text, Date, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase


class Base(DeclarativeBase):
    pass


author_school_table = Table(
    "author_school",
    Base.metadata,
    Column("author_id", ForeignKey("author.id"), primary_key=True),
    Column("school_id", ForeignKey("school.id"), primary_key=True),
)


class Author(Base):
    __tablename__ = "author"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    
    # ID externo de la API de filósofos
    external_id: Mapped[Optional[str]] = mapped_column(String, nullable=True, unique=True)
    
    # Información básica
    nombre: Mapped[str] = mapped_column(String, nullable=False)
    username: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    vida: Mapped[Optional[str]] = mapped_column(String, nullable=True)  # life field
    descripcion_topica: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    areas_interes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Fechas detalladas de la API
    fecha_nacimiento_completa: Mapped[Optional[str]] = mapped_column(String, nullable=True)  # "16 June 1723"
    fecha_muerte_completa: Mapped[Optional[str]] = mapped_column(String, nullable=True)     # "17 July 1790"
    año_nacimiento: Mapped[Optional[str]] = mapped_column(String, nullable=True)            # "1723 AD"
    año_muerte: Mapped[Optional[str]] = mapped_column(String, nullable=True)                # "1790 AD"
    
    # Fechas parseadas (para compatibilidad)
    fecha_nacimiento: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    fecha_defuncion: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    epoca: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    
    # Ubicación
    lugar_nacimiento: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    
    # Escuela filosófica principal
    escuela_principal: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    
    # Enlaces importantes
    enlace_iep: Mapped[Optional[str]] = mapped_column(String, nullable=True)        # Biografía principal
    enlace_stanford: Mapped[Optional[str]] = mapped_column(String, nullable=True)   # SEP
    titulo_wiki: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    
    # Imágenes (JSON con todas las variantes)
    imagenes: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    imagen_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)  # Para compatibilidad
    
    # Información sobre libros
    tiene_libros: Mapped[bool] = mapped_column(default=False)
    libros_librivox: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    
    # Biografía extraída
    biografia: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    schools: Mapped[List["School"]] = relationship(
        secondary=author_school_table, back_populates="authors"
    )
    books: Mapped[List["Book"]] = relationship(back_populates="author")
    quotes: Mapped[List["Quote"]] = relationship(back_populates="author")


class School(Base):
    __tablename__ = "school"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String, nullable=False)
    imagen_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    descripcion: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    authors: Mapped[List[Author]] = relationship(
        secondary=author_school_table, back_populates="schools"
    )


class Book(Base):
    __tablename__ = "book"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    
    # ID externo (para LibriVox)
    external_id: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    librivox_id: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    
    # Información básica
    titulo: Mapped[str] = mapped_column(String, nullable=False)
    descripcion: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Imágenes y enlaces
    imagen_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    cover_art_path: Mapped[Optional[str]] = mapped_column(String, nullable=True)  # De LibriVox
    librivox_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    
    # Tipo de libro
    es_audiolibro: Mapped[bool] = mapped_column(default=False)
    es_ebook: Mapped[bool] = mapped_column(default=False)
    
    # Relación con el autor
    autor_id: Mapped[Optional[int]] = mapped_column(ForeignKey("author.id"), nullable=True)
    author: Mapped[Optional[Author]] = relationship(back_populates="books")


class Quote(Base):
    __tablename__ = "quote"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    
    # ID externo de la API
    external_id: Mapped[Optional[str]] = mapped_column(String, nullable=True, unique=True)
    internal_id: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    
    # Contenido de la quote
    texto: Mapped[str] = mapped_column(Text, nullable=False)
    
    # Información sobre la fuente
    obra: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    año: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    
    # Relación con el autor
    autor_id: Mapped[Optional[int]] = mapped_column(ForeignKey("author.id"), nullable=True)
    author: Mapped[Optional[Author]] = relationship(back_populates="quotes")
    
    # ID externo del filósofo (para mapear con la API)
    philosopher_external_id: Mapped[Optional[str]] = mapped_column(String, nullable=True)


