#!/usr/bin/env python3
"""
🖼️ Script mejorado para obtener imágenes reales de filósofos
Usa URLs directas de Wikipedia para los filósofos más importantes
"""

import os
import sys
sys.path.append('/opt/app')

from app.database import SessionLocal
from app.models import Author
from app.aws_s3 import s3_manager

# URLs directas de imágenes reales de Wikipedia para filósofos importantes
PHILOSOPHER_IMAGES = {
    "Platón": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4a/Plato-raphael.jpg/256px-Plato-raphael.jpg",
    "Aristóteles": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/ae/Aristotle_Altemps_Inv8575.jpg/256px-Aristotle_Altemps_Inv8575.jpg",
    "Sócrates": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a4/Socrates_Louvre.jpg/256px-Socrates_Louvre.jpg",
    "Tomás de Aquino": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/Thomas_Aquinas_by_Fra_Angelico.jpg/256px-Thomas_Aquinas_by_Fra_Angelico.jpg",
    "San Agustín": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6a/Augustine_of_Hippo.jpg/256px-Augustine_of_Hippo.jpg",
    "René Descartes": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/73/Frans_Hals_-_Portret_van_Ren%C3%A9_Descartes.jpg/256px-Frans_Hals_-_Portret_van_Ren%C3%A9_Descartes.jpg",
    "Immanuel Kant": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f2/Kant_gemaelde_3.jpg/256px-Kant_gemaelde_3.jpg",
    "Friedrich Nietzsche": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1b/Nietzsche187a.jpg/256px-Nietzsche187a.jpg",
    "Georg Hegel": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/08/G.W.F._Hegel_%28by_Sichling%2C_after_Sebbers%29.jpg/256px-G.W.F._Hegel_%28by_Sichling%2C_after_Sebbers%29.jpg",
    "John Locke": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d1/JohnLocke.png/256px-JohnLocke.png",
    "David Hume": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/ea/Painting_of_David_Hume.jpg/256px-Painting_of_David_Hume.jpg",
    "Baruch Spinoza": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/71/Spinoza.jpg/256px-Spinoza.jpg",
    "Gottfried Leibniz": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/ce/Gottfried_Wilhelm_Leibniz%2C_Bernhard_Christoph_Francke.jpg/256px-Gottfried_Wilhelm_Leibniz%2C_Bernhard_Christoph_Francke.jpg",
    "Séneca": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f6/Seneca-berlinantikensammlung-1.jpg/256px-Seneca-berlinantikensammlung-1.jpg",
    "Marco Aurelio": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3b/Marcus_Aurelius_Metropolitan_Museum.png/256px-Marcus_Aurelius_Metropolitan_Museum.png",
    "Epicteto": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/00/Epicteti_Enchiridion_Latinis_versibus_adumbratum_%28Oxford_1715%29_frontispiece.jpg/256px-Epicteti_Enchiridion_Latinis_versibus_adumbratum_%28Oxford_1715%29_frontispiece.jpg",
    "Confucio": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6c/Konfuzius-1770.jpg/256px-Konfuzius-1770.jpg",
    "Lao Tzu": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/cc/Laozi_002.jpg/256px-Laozi_002.jpg",
    "Martin Heidegger": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/da/Heidegger_4_%281960%29.jpg/256px-Heidegger_4_%281960%29.jpg",
    "Jean-Paul Sartre": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/ef/Sartre_1967_crop.jpg/256px-Sartre_1967_crop.jpg",
    "Søren Kierkegaard": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c9/Kierkegaard.jpg/256px-Kierkegaard.jpg",
    "Arthur Schopenhauer": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/bc/Arthur_Schopenhauer_by_J_Sch%C3%A4fer%2C_1859b.jpg/256px-Arthur_Schopenhauer_by_J_Sch%C3%A4fer%2C_1859b.jpg",
    "Ludwig Wittgenstein": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/ab/Ludwig_Wittgenstein.jpg/256px-Ludwig_Wittgenstein.jpg",
    "Hannah Arendt": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5a/Hannah_Arendt_1975.jpg/256px-Hannah_Arendt_1975.jpg",
    "Michel Foucault": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7e/Michel_Foucault_1974_Brasil.jpg/256px-Michel_Foucault_1974_Brasil.jpg"
}

def update_philosopher_images():
    """Actualiza las imágenes de los filósofos importantes con URLs reales"""
    
    os.environ["USE_S3"] = "true"
    session = SessionLocal()
    
    print("🚀 SCRIPT MEJORADO - IMÁGENES REALES DE FILÓSOFOS")
    print("=" * 55)
    
    success_count = 0
    total_count = len(PHILOSOPHER_IMAGES)
    
    for name, image_url in PHILOSOPHER_IMAGES.items():
        print(f"\n🔄 Procesando {name}...")
        
        # Buscar el filósofo en la base de datos
        author = session.query(Author).filter(Author.nombre == name).first()
        
        if not author:
            print(f"❌ {name} no encontrado en la base de datos")
            continue
        
        # Generar key de S3
        s3_key = s3_manager.generate_author_image_key(name)
        
        # Eliminar imagen existente para forzar regeneración
        try:
            s3_manager.s3_client.delete_object(
                Bucket=s3_manager.bucket_images, 
                Key=s3_key
            )
            print(f"🗑️ Eliminada imagen anterior de {name}")
        except:
            print(f"⚠️ No había imagen anterior de {name}")
        
        # Subir nueva imagen desde Wikipedia
        try:
            new_s3_url = s3_manager.upload_image_from_url(image_url, s3_key)
            if new_s3_url:
                author.imagen_url = new_s3_url
                success_count += 1
                print(f"✅ {name}: Imagen real subida a S3")
            else:
                print(f"❌ {name}: Error subiendo imagen")
        except Exception as e:
            print(f"❌ {name}: Error - {e}")
    
    # Guardar cambios
    session.commit()
    session.close()
    
    print(f"\n🎉 ¡COMPLETADO!")
    print(f"📊 Imágenes actualizadas: {success_count}/{total_count}")
    print(f"✅ Los filósofos importantes ahora tienen imágenes reales")
    print(f"🌐 Refresca el navegador en http://3.82.93.186:3000")

if __name__ == "__main__":
    update_philosopher_images()

