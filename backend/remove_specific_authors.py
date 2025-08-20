#!/usr/bin/env python3
"""
Script para eliminar autores específicos por nombre
"""

import os
import sys
sys.path.append('/opt/app')

from app.database import SessionLocal
from app.models import Author, Quote, Book

# Lista de autores específicos a eliminar
AUTHORS_TO_REMOVE = [
    "Lin Chi",
    "Dong Shan"
]

def remove_specific_authors():
    """Elimina autores específicos de la base de datos"""
    
    session = SessionLocal()
    
    print(f"🗑️ ELIMINANDO AUTORES ESPECÍFICOS")
    print("=" * 40)
    
    try:
        removed_count = 0
        
        for name in AUTHORS_TO_REMOVE:
            print(f"\n🔄 Buscando {name}...")
            
            # Buscar el autor en la base de datos
            author = session.query(Author).filter(Author.nombre == name).first()
            
            if not author:
                print(f"❌ {name} no encontrado en la base de datos")
                continue
            
            print(f"✅ {name} encontrado - ID: {author.id}")
            
            # Eliminar citas del autor
            quotes_deleted = session.query(Quote).filter(Quote.autor_id == author.id).delete()
            print(f"   📝 {quotes_deleted} citas eliminadas")
            
            # Eliminar libros del autor  
            books_deleted = session.query(Book).filter(Book.autor_id == author.id).delete()
            print(f"   📚 {books_deleted} libros eliminados")
            
            # Eliminar autor (las relaciones many-to-many se eliminan automáticamente)
            session.delete(author)
            removed_count += 1
            print(f"✅ {name}: Autor eliminado exitosamente")
        
        # Commit cambios
        session.commit()
        
        print(f"\n🎉 ¡ELIMINACIÓN COMPLETADA!")
        print(f"📊 Autores eliminados: {removed_count}/{len(AUTHORS_TO_REMOVE)}")
        
        # Verificar resultado final
        remaining_authors = session.query(Author).count()
        print(f"📈 Autores restantes en la base de datos: {remaining_authors}")
        
    except Exception as e:
        print(f"❌ Error durante la eliminación: {e}")
        session.rollback()
    finally:
        session.close()

if __name__ == "__main__":
    remove_specific_authors()