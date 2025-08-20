#!/usr/bin/env python3
from app.database import SessionLocal
from app.models import Author

session = SessionLocal()
total = session.query(Author).count()
print(f"Total autores restantes: {total}")

lin_chi = session.query(Author).filter(Author.nombre == "Lin Chi").first()
dong_shan = session.query(Author).filter(Author.nombre == "Dong Shan").first()

print(f"Lin Chi eliminado: {'Si' if not lin_chi else 'No'}")
print(f"Dong Shan eliminado: {'Si' if not dong_shan else 'No'}")

session.close()