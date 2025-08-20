#!/usr/bin/env python3
"""
Script simple para actualizar imágenes de escuelas a UI Avatars mejoradas
"""

import sys
sys.path.append('.')

from app.database import SessionLocal
from app.models import School

def update_school_images():
    """Actualiza todas las escuelas para usar UI Avatars con estilos mejorados"""
    session = SessionLocal()
    
    try:
        schools = session.query(School).all()
        print(f"🎨 Actualizando imágenes para {len(schools)} escuelas...")
        
        # Mapeo de colores por tipo de escuela
        school_colors = {
            # Antiguas
            "Platonismo": "4A90E2",       # Azul clásico
            "Aristotelismo": "8B4513",    # Marrón académico  
            "Estoicismo": "2E8B57",       # Verde sabio
            "Epicureísmo": "FF6B6B",      # Rosa placer
            
            # Medievales
            "Escolástica": "800080",      # Púrpura religioso
            "Humanismo": "FF7F50",        # Coral humanista
            
            # Modernas
            "Racionalismo": "4169E1",     # Azul real
            "Empirismo": "228B22",        # Verde bosque
            "Idealismo": "9370DB",        # Violeta ideal
            "Materialismo": "CD853F",     # Marrón tierra
            "Utilitarismo": "32CD32",     # Verde lima
            "Deontología": "4682B4",      # Azul acero
            
            # Contemporáneas
            "Existencialismo": "2F4F4F",  # Gris oscuro existencial
            "Fenomenología": "6A5ACD",    # Azul pizarra
            "Marxismo": "DC143C",         # Rojo revolución
            "Feminismo": "DA70D6",        # Orquídea
            "Pragmatismo": "B8860B",      # Dorado oscuro
            "Positivismo": "4B0082",      # Índigo
            
            # Estructuralistas
            "Estructuralismo": "708090",  # Gris pizarra
            "Post-estructuralismo": "2F2F2F", # Gris carbón
            "Hermenéutica": "8B008B",     # Magenta oscuro
            "Analítica": "191970",        # Azul medianoche
            "Continental": "556B2F",      # Verde oliva
            
            # Orientales
            "Budismo": "FF8C00",          # Naranja oscuro
            "Confucianismo": "B22222",    # Rojo fuego
            "Taoísmo": "008B8B",          # Cian oscuro
            "Hinduismo": "FF4500",        # Rojo naranja
            
            # Otras
            "Nihilismo": "000000",        # Negro
            "Relativismo": "696969",      # Gris
            "Absolutismo": "FFFFFF",      # Blanco
            "Crítica": "8B0000"           # Rojo oscuro
        }
        
        updated_count = 0
        
        for school in schools:
            color = school_colors.get(school.nombre, "4A90E2")  # Azul por defecto
            
            # Crear URL mejorada con colores específicos y mejor tipografía
            new_url = f"https://ui-avatars.com/api/?name={school.nombre.replace(' ', '+')}&background={color}&color=fff&size=256&bold=true&font-size=0.5"
            
            # Actualizar solo si cambió
            if school.imagen_url != new_url:
                school.imagen_url = new_url
                updated_count += 1
                print(f"✅ {school.nombre:20} → #{color}")
        
        session.commit()
        print(f"\n🎉 Completado: {updated_count} escuelas actualizadas con colores temáticos")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        session.rollback()
        raise
    finally:
        session.close()

if __name__ == "__main__":
    update_school_images()