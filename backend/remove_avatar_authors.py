#!/usr/bin/env python3
"""
Script para eliminar autores que tienen avatares generados (ui-avatars.com) 
en lugar de imágenes reales de Wikipedia/S3
"""

import os
import sys
import requests
sys.path.append('/opt/app')

from app.database import SessionLocal
from app.models import Author, Quote, Book

def is_avatar_url(image_url):
    """Detecta si una URL es un avatar generado vs imagen real"""
    if not image_url:
        return False
    
    # Avatares de ui-avatars.com
    if 'ui-avatars.com' in image_url:
        return True
    
    # Imágenes de S3 muy pequeñas (posiblemente avatares subidos)
    if 's3.amazonaws.com' in image_url or 'cloudfront.net' in image_url:
        try:
            response = requests.head(image_url, timeout=10)
            if response.status_code == 200:
                content_length = response.headers.get('content-length')
                if content_length:
                    size_bytes = int(content_length)
                    size_kb = size_bytes / 1024
                    # Si la imagen es menor a 15 KB, probablemente es avatar
                    if size_kb < 15:
                        return True
        except:
            pass
    
    return False

def get_image_info(image_url):
    """Obtiene información de la imagen para análisis"""
    if not image_url:
        return "Sin imagen", 0
    
    if 'ui-avatars.com' in image_url:
        return "Avatar UI", 0
    
    try:
        response = requests.head(image_url, timeout=10)
        if response.status_code == 200:
            content_length = response.headers.get('content-length')
            if content_length:
                size_kb = int(content_length) / 1024
                if 'wikipedia' in image_url or size_kb > 15:
                    return f"Imagen real", size_kb
                else:
                    return f"Avatar S3", size_kb
            else:
                return "Sin tamaño", 0
        else:
            return f"Error {response.status_code}", 0
    except Exception as e:
        return f"Error: {str(e)[:20]}", 0

def analyze_authors():
    """Analiza todos los autores y clasifica sus imágenes"""
    
    session = SessionLocal()
    
    print("🔍 ANALIZANDO IMÁGENES DE AUTORES")
    print("=" * 50)
    
    try:
        authors = session.query(Author).order_by(Author.nombre).all()
        
        avatar_authors = []
        real_image_authors = []
        no_image_authors = []
        
        for i, author in enumerate(authors, 1):
            print(f"📊 Analizando {i:3d}/{len(authors)}: {author.nombre[:30]:<30}", end=" ")
            
            if not author.imagen_url:
                no_image_authors.append(author)
                print("❌ Sin imagen")
                continue
            
            info_type, size_kb = get_image_info(author.imagen_url)
            
            if is_avatar_url(author.imagen_url):
                avatar_authors.append(author)
                print(f"🎨 {info_type} ({size_kb:.1f}KB)")
            else:
                real_image_authors.append(author)
                print(f"📷 {info_type} ({size_kb:.1f}KB)")
        
        # Resumen
        print(f"\n📊 RESUMEN DE ANÁLISIS")
        print(f"👥 Total autores: {len(authors)}")
        print(f"📷 Imágenes reales: {len(real_image_authors)}")
        print(f"🎨 Avatares generados: {len(avatar_authors)}")
        print(f"❌ Sin imagen: {len(no_image_authors)}")
        
        # Lista de autores con avatares
        if avatar_authors:
            print(f"\n🎨 AUTORES CON AVATARES ({len(avatar_authors)}):")
            for author in avatar_authors:
                print(f"   - {author.nombre}")
        
        # Lista de autores con imágenes reales
        if real_image_authors:
            print(f"\n📷 AUTORES CON IMÁGENES REALES ({len(real_image_authors)}):")
            for author in real_image_authors[:10]:  # Solo primeros 10
                print(f"   - {author.nombre}")
            if len(real_image_authors) > 10:
                print(f"   ... y {len(real_image_authors) - 10} más")
        
        return avatar_authors, real_image_authors, no_image_authors
        
    except Exception as e:
        print(f"❌ Error durante análisis: {e}")
        return [], [], []
    finally:
        session.close()

def remove_avatar_authors():
    """Elimina autores que solo tienen avatares generados"""
    
    print("\n🗑️ ELIMINANDO AUTORES CON AVATARES")
    print("=" * 40)
    
    # Primero analizar
    avatar_authors, real_image_authors, no_image_authors = analyze_authors()
    
    if not avatar_authors:
        print("✅ No hay autores con avatares para eliminar")
        return
    
    # Confirmar eliminación
    print(f"\n⚠️ Se eliminarán {len(avatar_authors)} autores con avatares")
    print("¿Continuar? Esta acción no se puede deshacer.")
    
    session = SessionLocal()
    
    try:
        removed_count = 0
        
        for author in avatar_authors:
            print(f"🗑️ Eliminando: {author.nombre}")
            
            # Eliminar citas del autor
            quotes_deleted = session.query(Quote).filter(Quote.autor_id == author.id).delete()
            print(f"   📝 {quotes_deleted} citas eliminadas")
            
            # Eliminar libros del autor  
            books_deleted = session.query(Book).filter(Book.autor_id == author.id).delete()
            print(f"   📚 {books_deleted} libros eliminados")
            
            # Eliminar autor
            session.delete(author)
            removed_count += 1
        
        # Commit cambios
        session.commit()
        
        print(f"\n✅ Eliminados {removed_count} autores con avatares")
        
        # Verificar resultado final
        remaining_authors = session.query(Author).count()
        print(f"📊 Autores restantes: {remaining_authors}")
        
        # Verificar que solo quedan autores con imágenes reales
        remaining_with_real_images = len([a for a in session.query(Author).all() 
                                        if a.imagen_url and not is_avatar_url(a.imagen_url)])
        print(f"📷 Autores con imágenes reales: {remaining_with_real_images}")
        
    except Exception as e:
        print(f"❌ Error durante eliminación: {e}")
        session.rollback()
    finally:
        session.close()

def main():
    """Función principal - permite elegir análisis o eliminación"""
    
    if len(sys.argv) > 1 and sys.argv[1] == '--remove':
        remove_avatar_authors()
    else:
        print("🔍 MODO ANÁLISIS - Solo mostrar información")
        print("Para eliminar, ejecutar: python script.py --remove")
        print()
        analyze_authors()

if __name__ == "__main__":
    main()