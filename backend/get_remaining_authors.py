#!/usr/bin/env python3
"""
Script para obtener los nombres de los 77 autores restantes
"""

import os
import sys
sys.path.append('/opt/app')

from app.database import SessionLocal
from app.models import Author

def get_remaining_authors():
    """Obtiene la lista de los 77 autores restantes para actualizar el seed"""
    
    session = SessionLocal()
    
    print("📝 OBTENIENDO LISTA DE AUTORES RESTANTES")
    print("=" * 50)
    
    try:
        # Obtener todos los autores restantes ordenados por nombre
        authors = session.query(Author).order_by(Author.nombre).all()
        
        print(f"📊 Total autores: {len(authors)}")
        print(f"\n📝 LISTA PARA AUTHOR_NAMES:")
        print("AUTHOR_NAMES = [")
        
        # Crear líneas de 5 nombres cada una para mantener formato legible
        names = [f'"{author.nombre}"' for author in authors]
        
        for i in range(0, len(names), 5):
            line_names = names[i:i+5]
            line = "    " + ", ".join(line_names)
            if i + 5 < len(names):
                line += ","
            print(line)
        
        print("]")
        
        print(f"\n✅ Lista generada con {len(authors)} autores")
        print("Copia esta lista y reemplázala en seed.py")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    get_remaining_authors()