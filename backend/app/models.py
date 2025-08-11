from __future__ import annotations

from datetime import date
from typing import Optional, List

from sqlalchemy import String, Integer, ForeignKey, Table, Column, Text, Date
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
    nombre: Mapped[str] = mapped_column(String, nullable=False)
    epoca: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    fecha_nacimiento: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    fecha_defuncion: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    imagen_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
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
    titulo: Mapped[str] = mapped_column(String, nullable=False)
    imagen_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    descripcion: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    autor_id: Mapped[int] = mapped_column(ForeignKey("author.id"))
    author: Mapped[Optional[Author]] = relationship(back_populates="books")


class Quote(Base):
    __tablename__ = "quote"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    texto: Mapped[str] = mapped_column(Text, nullable=False)
    autor_id: Mapped[int] = mapped_column(ForeignKey("author.id"))
    author: Mapped[Optional[Author]] = relationship(back_populates="quotes")


