from __future__ import annotations

import os
from typing import List

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from .database import create_db_and_tables, engine
from .seed import seed_data_if_needed, ensure_author_images, ensure_school_images, ensure_book_covers, fix_generic_book_titles
from .routers import authors, books, schools, quotes, stats


def get_cors_origins_from_env() -> List[str]:
    raw = os.getenv("CORS_ORIGINS", "*")
    # Allow comma-separated list; trim spaces
    origins = [o.strip() for o in raw.split(",") if o.strip()]
    return origins


app = FastAPI(title="Biblioteca de Filosofía API", version="1.0.0")


# CORS
origins = get_cors_origins_from_env()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar dominios específicos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(authors.router)
app.include_router(books.router)
app.include_router(schools.router)
app.include_router(quotes.router)
app.include_router(stats.router)

@app.get("/")
def read_root():
    return {"message": "Bienvenido a la Biblioteca de Filosofía API"}

@app.on_event("startup")
def on_startup() -> None:
    create_db_and_tables()
    with Session(engine) as session:
        seed_data_if_needed(session)
        ensure_author_images(session)
        ensure_school_images(session)
        fix_generic_book_titles(session)  # Arreglar títulos genéricos primero
        ensure_book_covers(session)       # Luego actualizar portadas


@app.get("/health", tags=["health"]) 
def healthcheck() -> dict:
    return {"status": "ok"}


