#!/usr/bin/env python3
from app.database import SessionLocal
from app.models import Author

def main():
    session = SessionLocal()
    try:
        total = session.query(Author).count()
        authors = session.query(Author).order_by(Author.nombre).all()
        
        print(f"📊 Total autores en producción: {total}")
        print("\n📝 Lista completa de autores:")
        print("-" * 40)
        
        arab_count = 0
        for i, author in enumerate(authors, 1):
            is_arab = any(prefix in author.nombre for prefix in ['Al-', 'Ibn ', 'Avicena', 'Averroes', 'Maimonides'])
            if is_arab:
                arab_count += 1
                print(f"{i:3d}. {author.nombre} [ÁRABE]")
            else:
                print(f"{i:3d}. {author.nombre}")
        
        print(f"\n🕌 Total autores árabes: {arab_count}")
        
    finally:
        session.close()

if __name__ == "__main__":
    main()