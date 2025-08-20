#!/usr/bin/env python3
"""
Script para obtener imágenes reales de Wikipedia para escuelas filosóficas
"""

import sys
sys.path.append('.')

from app.database import SessionLocal
from app.models import School

def get_wikipedia_school_images():
    """URLs de imágenes reales de Wikipedia para escuelas filosóficas"""
    
    SCHOOL_WIKIPEDIA_IMAGES = {
        # Filosofía Antigua
        "Platonismo": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4a/Plato-raphael.jpg/800px-Plato-raphael.jpg",
        "Aristotelismo": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/ae/Aristotle_Altemps_Inv8575.jpg/800px-Aristotle_Altemps_Inv8575.jpg", 
        "Estoicismo": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/ea/Stoa_of_Attalus_Athens.jpg/800px-Stoa_of_Attalus_Athens.jpg",
        "Epicureísmo": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/88/Epicurus_bust2.jpg/800px-Epicurus_bust2.jpg",
        
        # Filosofía Medieval
        "Escolástica": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f0/Thomas-von-aquin.jpg/800px-Thomas-von-aquin.jpg",
        "Humanismo": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0e/Pico_della_Mirandola.jpg/800px-Pico_della_Mirandola.jpg",
        
        # Filosofía Moderna
        "Racionalismo": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/73/Frans_Hals_-_Portret_van_René_Descartes.jpg/800px-Frans_Hals_-_Portret_van_René_Descartes.jpg",
        "Empirismo": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d1/JohnLocke.png/800px-JohnLocke.png",
        "Idealismo": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f2/Kant_foto.jpg/800px-Kant_foto.jpg",
        "Materialismo": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/Karl_Marx_001.jpg/800px-Karl_Marx_001.jpg",
        "Utilitarismo": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c8/Jeremy_Bentham_by_Henry_William_Pickersgill_detail.jpg/800px-Jeremy_Bentham_by_Henry_William_Pickersgill_detail.jpg",
        "Deontología": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f2/Kant_foto.jpg/800px-Kant_foto.jpg",
        
        # Filosofía Contemporánea
        "Existencialismo": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/ef/Sartre_1967_crop.jpg/800px-Sartre_1967_crop.jpg",
        "Fenomenología": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a0/Edmund_Husserl_1900.jpg/800px-Edmund_Husserl_1900.jpg",
        "Marxismo": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/Karl_Marx_001.jpg/800px-Karl_Marx_001.jpg",
        "Feminismo": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/33/Simone_de_Beauvoir2.jpg/800px-Simone_de_Beauvoir2.jpg",
        "Pragmatismo": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/56/William_James_b1842c.jpg/800px-William_James_b1842c.jpg",
        "Positivismo": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3c/Auguste_Comte.jpg/800px-Auguste_Comte.jpg",
        
        # Estructuralismo y Post-estructuralismo
        "Estructuralismo": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c0/Claude_L%C3%A9vi-Strauss_-_Seuil_1967.png/800px-Claude_L%C3%A9vi-Strauss_-_Seuil_1967.png",
        "Post-estructuralismo": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/77/Foucault5.jpg/800px-Foucault5.jpg",
        "Hermenéutica": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6e/Gadamer.jpg/800px-Gadamer.jpg",
        "Analítica": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/be/Bertrand_Russell_transparent_bg.png/800px-Bertrand_Russell_transparent_bg.png",
        "Continental": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/da/Heidegger_4_%281960%29_cropped.jpg/800px-Heidegger_4_%281960%29_cropped.jpg",
        
        # Filosofías Orientales
        "Budismo": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f0/Buddha_statue_in_Bodhgaya.jpg/800px-Buddha_statue_in_Bodhgaya.jpg",
        "Confucianismo": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1c/Confucius_02.png/800px-Confucius_02.png",
        "Taoísmo": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f0/Laozi_by_Zhang_Lu.jpg/800px-Laozi_by_Zhang_Lu.jpg",
        "Hinduismo": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/14/Adi_Shankara.jpg/800px-Adi_Shankara.jpg",
        
        # Otras corrientes
        "Nihilismo": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1b/Nietzsche187a.jpg/800px-Nietzsche187a.jpg",
        "Relativismo": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4a/Protagoras_Nuremberg_Chronicle.jpg/800px-Protagoras_Nuremberg_Chronicle.jpg",
        "Absolutismo": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/50/Plato_Silanion_Musei_Capitolini_MC1377.jpg/800px-Plato_Silanion_Musei_Capitolini_MC1377.jpg",
        "Crítica": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/Karl_Marx_001.jpg/800px-Karl_Marx_001.jpg"
    }
    
    session = SessionLocal()
    
    try:
        schools = session.query(School).all()
        print(f"🖼️ Actualizando imágenes de Wikipedia para {len(schools)} escuelas...")
        
        updated_count = 0
        
        for school in schools:
            if school.nombre in SCHOOL_WIKIPEDIA_IMAGES:
                new_url = SCHOOL_WIKIPEDIA_IMAGES[school.nombre]
                school.imagen_url = new_url
                updated_count += 1
                print(f"✅ {school.nombre:20} → Wikipedia image")
            else:
                # Fallback a UI Avatar solo si no hay imagen de Wikipedia
                fallback_url = f"https://ui-avatars.com/api/?name={school.nombre.replace(' ', '+')}&background=4A90E2&color=fff&size=256&bold=true"
                school.imagen_url = fallback_url  
                print(f"⚠️ {school.nombre:20} → Fallback (no Wikipedia image found)")
        
        session.commit()
        print(f"\n🎉 Completado: {updated_count} escuelas con imágenes reales de Wikipedia")
        
        # Mostrar algunas URLs de ejemplo
        print(f"\n📸 Ejemplos de imágenes:")
        for school in schools[:5]:
            print(f"   {school.nombre}: {school.imagen_url}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        session.rollback()
        raise
    finally:
        session.close()

if __name__ == "__main__":
    get_wikipedia_school_images()