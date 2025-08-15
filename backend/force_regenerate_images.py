#!/usr/bin/env python3
"""
Script para forzar la regeneración de TODAS las imágenes
Reemplaza avatares con imágenes reales de Wikipedia
"""

import os
import sys
sys.path.append('/opt/app')

from app.database import SessionLocal
from app.models import Author, School, Book
from app.seed import author_image_url, school_image_url

def force_regenerate_all_images():
    """Fuerza la regeneración de todas las imágenes"""
    os.environ["USE_S3"] = "true"
    
    session = SessionLocal()
    
    print("🔥 REGENERACIÓN FORZADA DE TODAS LAS IMÁGENES")
    print("=" * 50)
    
    # AUTORES
    authors = session.query(Author).all()
    print(f"\n📚 Procesando {len(authors)} AUTORES...")
    
    author_success = 0
    author_wikipedia = 0
    
    for i, author in enumerate(authors):
        if i % 50 == 0:
            print(f"✅ Procesados {i}/{len(authors)} autores...")
        
        try:
            # FORZAR nueva imagen
            new_url = author_image_url(author.nombre)
            if new_url:
                old_url = author.imagen_url
                author.imagen_url = new_url
                author_success += 1
                
                # Detectar si es Wikipedia vs Avatar
                if "wikimedia" in new_url or "wikipedia" in new_url:
                    author_wikipedia += 1
                    if i < 20:  # Mostrar primeros 20
                        print(f"🖼️ {author.nombre}: Wikipedia ✅")
                elif i < 20:  # Mostrar primeros 20
                    print(f"🎨 {author.nombre}: Avatar generado")
                    
        except Exception as e:
            if i < 10:  # Solo mostrar primeros errores
                print(f"❌ Error con {author.nombre}: {e}")
    
    # ESCUELAS
    schools = session.query(School).all()
    print(f"\n🏛️ Procesando {len(schools)} ESCUELAS...")
    
    school_success = 0
    
    for school in schools:
        try:
            new_url = school_image_url(school.nombre)
            if new_url:
                school.imagen_url = new_url
                school_success += 1
        except Exception as e:
            print(f"❌ Error con escuela {school.nombre}: {e}")
    
    # COMMIT TODO
    session.commit()
    
    print(f"\n🎉 ¡REGENERACIÓN COMPLETADA!")
    print(f"📊 Autores actualizados: {author_success}/{len(authors)}")
    print(f"🖼️ Imágenes de Wikipedia: {author_wikipedia}")
    print(f"🎨 Avatares generados: {author_success - author_wikipedia}")
    print(f"🏛️ Escuelas actualizadas: {school_success}/{len(schools)}")
    
    session.close()

if __name__ == "__main__":
    force_regenerate_all_images()
