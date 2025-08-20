from __future__ import annotations

import os
from typing import List

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from .database import create_db_and_tables, engine
from .seed import seed_data_if_needed
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
    allow_origins=origins if origins != ["*"] else [
        "http://localhost:3000",          # Frontend desarrollo local
        "http://localhost:8000",          # Backend desarrollo local
        "http://3.82.93.186:3000",        # Tu servidor EC2 actual
        "http://3.82.93.186:8000",        # API EC2 actual
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
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
    print("🚀 MAIN.PY STARTUP EJECUTÁNDOSE...")
    create_db_and_tables()
    print("🚀 CREANDO SESIÓN Y LLAMANDO SEED...")
    with Session(engine) as session:
        seed_data_if_needed(session)
    print("🚀 SEED COMPLETADO...")
        # Comentamos temporalmente las funciones que descargan imágenes
        # para permitir que la aplicación arranque más rápido
        # ensure_author_images(session)
        # ensure_school_images(session)
        # fix_generic_book_titles(session)  # Arreglar títulos genéricos primero
        # ensure_book_covers(session)       # Luego actualizar portadas


@app.get("/health", tags=["health"]) 
def healthcheck() -> dict:
    return {"status": "ok"}


