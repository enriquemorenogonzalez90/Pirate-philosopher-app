#!/usr/bin/env python3
"""
Script para verificar qué autores hay en la base de datos
"""

import os
import sys
sys.path.append('/opt/app')

from app.database import SessionLocal
from app.models import Author

def check_current_authors():
    """Verifica qué autores hay actualmente en la base de datos"""
    
    session = SessionLocal()
    
    print("📋 AUTORES ACTUALES EN LA BASE DE DATOS")
    print("=" * 50)
    
    try:
        authors = session.query(Author).order_by(Author.nombre).all()
        
        print(f"📊 Total de autores: {len(authors)}")
        print("\n📝 Lista de autores:")
        print("-" * 30)
        
        for i, author in enumerate(authors, 1):
            print(f"{i:3d}. {author.nombre}")
        
        # Verificar si hay autores árabes
        arab_authors = [author for author in authors if any(prefix in author.nombre for prefix in ['Al-', 'Ibn ', 'Avicena', 'Averroes', 'Maimonides'])]
        
        if arab_authors:
            print(f"\n🕌 Autores árabes encontrados ({len(arab_authors)}):")
            for author in arab_authors:
                print(f"   - {author.nombre}")
        else:
            print("\n✅ No se encontraron autores árabes en la base de datos")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    check_current_authors()