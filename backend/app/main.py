from __future__ import annotations

import os
from typing import List

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from .models.database import engine
from .models.models import Base
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
    # Crear todas las tablas
    Base.metadata.create_all(bind=engine)
    print("🚀 TABLAS CREADAS...")
    
    # Verificar si hay datos JSON y hacer seed básico
    from pathlib import Path
    import json
    
    data_dir = Path(__file__).parent / "data" / "json"
    philosophers_file = data_dir / "philosophers_complete_data.json"
    
    if philosophers_file.exists():
        print("🚀 ARCHIVOS JSON ENCONTRADOS - Iniciando seed automático...")
        try:
            from .models.database import SessionLocal
            from .models.models import Author
            
            with SessionLocal() as session:
                if session.query(Author).count() == 0:
                    print("🚀 EJECUTANDO SEED BÁSICO...")
                    # Importar y ejecutar seed
                    try:
                        import sys
                        sys.path.append(str(Path(__file__).parent / "data" / "scripts"))
                        from .data.scripts.seed import PhilosopherSeeder
                        seeder = PhilosopherSeeder(session)
                        seeder.seed_all()
                        session.commit()
                    except Exception as seed_error:
                        print(f"⚠️ Error en seed detallado: {seed_error}")
                        import traceback
                        traceback.print_exc()
                else:
                    print("🚀 DATOS YA EXISTENTES")
        except Exception as e:
            print(f"⚠️ Error en seed automático: {e}")
    else:
        print("🚀 No se encontraron archivos JSON - Ejecutar extract_philosophers.py primero")
    
    print("🚀 BACKEND LISTO")


@app.get("/health", tags=["health"]) 
def healthcheck() -> dict:
    return {"status": "ok"}


