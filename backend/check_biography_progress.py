#!/usr/bin/env python3
from app.database import SessionLocal
from app.models import Author

session = SessionLocal()
total = session.query(Author).count()
with_placeholder = session.query(Author).filter(Author.biografia.like('% fue un filósofo influyente.')).count()
with_real_bio = total - with_placeholder

print(f"📊 PROGRESO DE BIOGRAFÍAS")
print(f"Total autores: {total}")
print(f"Con biografías reales: {with_real_bio}")
print(f"Con biografías placeholder: {with_placeholder}")
print(f"Progreso: {(with_real_bio/total*100):.1f}%")

session.close()