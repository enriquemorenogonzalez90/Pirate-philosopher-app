#!/usr/bin/env python3
"""
Script para eliminar autores árabes de la base de datos
"""

import os
import sys
sys.path.append('/opt/app')

from app.database import SessionLocal
from app.models import Author, Book, Quote

# Lista de nombres de filósofos árabes a eliminar
ARAB_AUTHORS = [
    "Al-Kindi", "Al-Farabi", "Avicena", "Al-Ghazali", "Averroes",
    "Ibn Khaldun", "Al-Razi", "Ibn Sina", "Ibn Rushd", "Mulla Sadra",
    "Suhrawardi", "Ibn Arabi", "Al-Jahiz", "Al-Tabari", "Maimonides",
    "Al-Hallaj", "Ibn Taymiyyah", "Al-Ash'ari", "Al-Maturidi", "Ibn Hazm",
    "Al-Baqillani", "Al-Juwaini", "Al-Baghdadi", "Ibn Qudamah", "Al-Nawawi",
    "Ibn Qayyim", "Al-Dhahabi", "Al-Suyuti", "Ibn Hajar", "Al-Shatibi",
    "Al-Tusi", "Ibn Masarra", "Ibn Bajjah", "Ibn Tufail", "Al-Bitruji",
    "Ibn Sabʿin", "Al-Shushtari", "Ibn Qasi", "Ibn Barajan", "Al-Urfi"
]

def remove_arab_authors():
    """Elimina autores árabes de la base de datos"""
    
    session = SessionLocal()
    
    print("🗑️ ELIMINANDO AUTORES ÁRABES")
    print("=" * 40)
    
    removed_count = 0
    total_arab_authors = len(ARAB_AUTHORS)
    
    try:
        for name in ARAB_AUTHORS:
            print(f"\n🔄 Buscando {name}...")
            
            # Buscar el autor en la base de datos
            author = session.query(Author).filter(Author.nombre == name).first()
            
            if not author:
                print(f"⚠️ {name} no encontrado en la base de datos")
                continue
            
            # Eliminar citas del autor
            quotes_deleted = session.query(Quote).filter(Quote.autor_id == author.id).delete()
            print(f"🗑️ {name}: {quotes_deleted} citas eliminadas")
            
            # Eliminar libros del autor
            books_deleted = session.query(Book).filter(Book.autor_id == author.id).delete()
            print(f"📚 {name}: {books_deleted} libros eliminados")
            
            # Eliminar el autor (las relaciones many-to-many se eliminan automáticamente)
            session.delete(author)
            removed_count += 1
            print(f"✅ {name}: Autor eliminado")
        
        # Confirmar cambios
        session.commit()
        
        print(f"\n🎉 ¡ELIMINACIÓN COMPLETADA!")
        print(f"📊 Autores eliminados: {removed_count}/{total_arab_authors}")
        
        # Mostrar estadísticas finales
        remaining_authors = session.query(Author).count()
        print(f"📈 Autores restantes en la base de datos: {remaining_authors}")
        
    except Exception as e:
        print(f"❌ Error durante la eliminación: {e}")
        session.rollback()
    finally:
        session.close()

if __name__ == "__main__":
    remove_arab_authors()