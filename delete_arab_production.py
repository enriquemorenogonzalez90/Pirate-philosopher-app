#!/usr/bin/env python3
from app.database import SessionLocal
from app.models import Author, Quote, Book

# Lista de filósofos árabes a eliminar
ARAB_PHILOSOPHERS = [
    "Al-Kindi", "Al-Farabi", "Avicena", "Al-Ghazali", "Averroes",
    "Ibn Khaldun", "Al-Razi", "Ibn Sina", "Ibn Rushd", "Mulla Sadra",
    "Suhrawardi", "Ibn Arabi", "Al-Jahiz", "Al-Tabari", "Maimonides",
    "Al-Hallaj", "Ibn Taymiyyah", "Al-Ash'ari", "Al-Maturidi", "Ibn Hazm",
    "Al-Baqillani", "Al-Juwaini", "Al-Baghdadi", "Ibn Qudamah", "Al-Nawawi",
    "Ibn Qayyim", "Al-Dhahabi", "Al-Suyuti", "Ibn Hajar", "Al-Shatibi",
    "Al-Tusi", "Ibn Masarra", "Ibn Bajjah", "Ibn Tufail", "Al-Bitruji",
    "Ibn Sabʿin", "Al-Shushtari", "Ibn Qasi", "Ibn Barajan", "Al-Urfi"
]

def main():
    print("🗑️ Eliminando filósofos árabes de la base de datos...")
    
    session = SessionLocal()
    
    try:
        # 1. Encontrar autores árabes
        arab_authors = session.query(Author).filter(Author.nombre.in_(ARAB_PHILOSOPHERS)).all()
        
        print(f"📊 Encontrados {len(arab_authors)} filósofos árabes")
        
        removed_count = 0
        
        for author in arab_authors:
            print(f"🗑️ Eliminando: {author.nombre}")
            
            # 2. Eliminar citas del autor
            quotes_deleted = session.query(Quote).filter(Quote.autor_id == author.id).delete()
            print(f"   📝 {quotes_deleted} citas eliminadas")
            
            # 3. Eliminar libros del autor  
            books_deleted = session.query(Book).filter(Book.autor_id == author.id).delete()
            print(f"   📚 {books_deleted} libros eliminados")
            
            # 4. Eliminar autor (las relaciones many-to-many se eliminan automáticamente)
            session.delete(author)
            removed_count += 1
        
        # 5. Commit cambios
        session.commit()
        
        print(f"\n✅ Eliminados {removed_count} filósofos árabes y sus datos relacionados")
        
        # Verificar resultado final
        remaining_authors = session.query(Author).count()
        print(f"📊 Autores restantes en la base de datos: {remaining_authors}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        session.rollback()
    finally:
        session.close()

    print("🎯 Operación completada!")

if __name__ == "__main__":
    main()