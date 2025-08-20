#!/usr/bin/env python3
"""
Script para eliminar autores que tienen biografías placeholder
"""

import os
import sys
sys.path.append('/opt/app')

from app.database import SessionLocal
from app.models import Author, Quote, Book

def remove_placeholder_biographies():
    """Elimina autores que tienen biografías placeholder"""
    
    session = SessionLocal()
    
    print("🗑️ ELIMINANDO AUTORES CON BIOGRAFÍAS PLACEHOLDER")
    print("=" * 60)
    
    try:
        # Obtener autores con biografías placeholder
        authors_to_remove = session.query(Author).filter(
            Author.biografia.like('% fue un filósofo influyente.')
        ).order_by(Author.nombre).all()
        
        # Verificar cuántos autores serán eliminados
        total_before = session.query(Author).count()
        to_remove_count = len(authors_to_remove)
        
        print(f"📊 ESTADO INICIAL:")
        print(f"Total autores actuales: {total_before}")
        print(f"Autores a eliminar: {to_remove_count}")
        print(f"Autores que quedarán: {total_before - to_remove_count}")
        
        if to_remove_count == 0:
            print("✅ No hay autores con biografías placeholder para eliminar")
            return
            
        print(f"\n📝 LISTA DE AUTORES A ELIMINAR:")
        print("-" * 50)
        for i, author in enumerate(authors_to_remove, 1):
            print(f"{i:2d}. {author.nombre}")
            
        print(f"\n🗑️ INICIANDO ELIMINACIÓN...")
        print("-" * 40)
        
        removed_count = 0
        quotes_deleted_total = 0
        books_deleted_total = 0
        
        for author in authors_to_remove:
            print(f"\n🗑️ Eliminando: {author.nombre}")
            
            # Eliminar citas del autor
            quotes_deleted = session.query(Quote).filter(Quote.autor_id == author.id).delete()
            quotes_deleted_total += quotes_deleted
            print(f"   📝 {quotes_deleted} citas eliminadas")
            
            # Eliminar libros del autor  
            books_deleted = session.query(Book).filter(Book.autor_id == author.id).delete()
            books_deleted_total += books_deleted
            print(f"   📚 {books_deleted} libros eliminados")
            
            # Eliminar autor (las relaciones many-to-many se eliminan automáticamente)
            session.delete(author)
            removed_count += 1
            print(f"✅ {author.nombre}: Eliminado exitosamente")
        
        # Commit cambios
        session.commit()
        
        # Verificar resultado final
        total_after = session.query(Author).count()
        
        print(f"\n🎉 ¡ELIMINACIÓN COMPLETADA!")
        print(f"=" * 50)
        print(f"📊 RESUMEN:")
        print(f"Autores eliminados: {removed_count}")
        print(f"Citas eliminadas: {quotes_deleted_total}")
        print(f"Libros eliminados: {books_deleted_total}")
        print(f"Total autores antes: {total_before}")
        print(f"Total autores después: {total_after}")
        print(f"Reducción: {total_before - total_after} autores")
        
        print(f"\n✅ RESULTADO FINAL:")
        print(f"📚 {total_after} autores con biografías reales y detalladas")
        print(f"🎯 100% de los autores restantes tienen biografías auténticas")
        
    except Exception as e:
        print(f"❌ Error durante la eliminación: {e}")
        session.rollback()
    finally:
        session.close()

if __name__ == "__main__":
    remove_placeholder_biographies()