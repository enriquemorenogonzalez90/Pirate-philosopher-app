#!/usr/bin/env python3
"""
Script para regenerar imágenes de escuelas filosóficas
"""

import os
import sys
sys.path.append('.')

from app.database import SessionLocal
from app.models import School
from app.aws_s3 import s3_manager
import urllib.parse

def fix_school_images():
    """Regenera todas las imágenes de escuelas usando UI Avatars y S3"""
    session = SessionLocal()
    
    try:
        schools = session.query(School).all()
        print(f"🔧 Regenerando imágenes para {len(schools)} escuelas...")
        
        updated_count = 0
        
        for school in schools:
            print(f"\n📚 Procesando: {school.nombre}")
            
            # Generar nueva imagen con UI Avatars y subirla a S3
            s3_key = s3_manager.generate_school_image_key(school.nombre)
            avatar_url = f"https://ui-avatars.com/api/?name={school.nombre.replace(' ', '+')}&background=blue&color=white&size=300&bold=true"
            
            print(f"   🎨 UI Avatar URL: {avatar_url}")
            print(f"   🔑 S3 Key: {s3_key}")
            
            # Subir imagen a S3
            s3_url = s3_manager.upload_image_from_url(avatar_url, s3_key)
            
            if s3_url:
                # Crear URL final
                encoded_key = urllib.parse.quote(s3_key, safe='/')
                cloudfront_domain = os.getenv('CLOUDFRONT_DOMAIN', '')
                
                if cloudfront_domain:
                    final_url = f"{cloudfront_domain}/{encoded_key}"
                else:
                    bucket = os.getenv('S3_BUCKET_IMAGES', 'filosofia-app-images')
                    final_url = f"https://{bucket}.s3.amazonaws.com/{encoded_key}"
                
                # Actualizar en base de datos
                school.imagen_url = final_url
                updated_count += 1
                print(f"   ✅ Actualizada: {final_url}")
            else:
                # Fallback a UI Avatars directamente
                school.imagen_url = avatar_url
                updated_count += 1
                print(f"   ⚠️ Fallback: {avatar_url}")
        
        session.commit()
        print(f"\n🎉 Completado: {updated_count} escuelas actualizadas")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        session.rollback()
        raise
    finally:
        session.close()

if __name__ == "__main__":
    fix_school_images()