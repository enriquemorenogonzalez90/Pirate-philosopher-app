from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

# URL de la base de datos desde variable de entorno (requerida)
DATABASE_URL = os.getenv("DATABASE_URL")

# Configurar el engine
engine = create_engine(DATABASE_URL)

# Session local
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency para obtener sesión de BD
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()