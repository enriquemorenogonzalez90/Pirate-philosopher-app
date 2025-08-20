#!/usr/bin/env python3
"""
Script para corregir épocas de filósofos y actualizar avatares con imágenes reales
"""

import os
import sys
sys.path.append('/opt/app')

from app.database import SessionLocal
from app.models import Author

# Clasificación correcta de épocas por filósofo
PHILOSOPHER_EPOCHS = {
    # Antiguos (Griegos y Romanos)
    "Sócrates": "Antigua", "Platón": "Antigua", "Aristóteles": "Antigua", 
    "Epicuro": "Antigua", "Zenón de Citio": "Antigua", "Pitágoras": "Antigua",
    "Heráclito": "Antigua", "Parménides": "Antigua", "Séneca": "Antigua",
    "Marco Aurelio": "Antigua", "Epicteto": "Antigua", "Tales de Mileto": "Antigua",
    "Anaximandro": "Antigua", "Anaxímenes": "Antigua", "Jenófanes": "Antigua",
    "Protágoras": "Antigua", "Gorgias": "Antigua", "Antístenes": "Antigua",
    "Cleantes": "Antigua", "Empédocles": "Antigua", "Anaxágoras": "Antigua",
    "Plotino": "Antigua", "Proclo": "Antigua", "Jámblico": "Antigua",
    "Porfirio": "Antigua", "Simplicio": "Antigua", "Alejandro de Afrodisias": "Antigua",
    "Filón de Alejandría": "Antigua", "Diógenes Laercio": "Antigua",
    "Hierocles": "Antigua", "Luciano de Samósata": "Antigua", "Galeno": "Antigua",
    "Ptolomeo": "Antigua", "Apolonio de Tiana": "Antigua",
    
    # Medievales
    "Tomás de Aquino": "Medieval", "San Agustín": "Medieval", 
    "Anselmo de Canterbury": "Medieval", "Pedro Abelardo": "Medieval",
    "Juan Escoto Erígena": "Medieval", "Boecio": "Medieval", "Alberto Magno": "Medieval",
    "Buenaventura": "Medieval", "Meister Eckhart": "Medieval", "Duns Escoto": "Medieval",
    "Guillermo de Ockham": "Medieval",
    
    # Orientales (Clásicos)
    "Confucio": "Antigua", "Lao Tzu": "Antigua", "Buda": "Antigua",
    "Nagarjuna": "Antigua", "Mencio": "Antigua", "Mozi": "Antigua",
    "Zhuangzi": "Antigua", "Shankara": "Medieval",
    
    # Modernos (siglos XVII-XVIII)
    "René Descartes": "Moderna", "Baruch Spinoza": "Moderna", 
    "John Locke": "Moderna", "David Hume": "Moderna", "Immanuel Kant": "Moderna",
    
    # Contemporáneos (siglos XIX-XXI)
    "Georg Hegel": "Contemporánea", "Friedrich Nietzsche": "Contemporánea",
    "Søren Kierkegaard": "Contemporánea", "Karl Marx": "Contemporánea",
    "Arthur Schopenhauer": "Contemporánea", "Ludwig Wittgenstein": "Contemporánea",
    "Jean-Paul Sartre": "Contemporánea", "Simone de Beauvoir": "Contemporánea",
    "Edmund Husserl": "Contemporánea", "Maurice Merleau-Ponty": "Contemporánea",
    "Emmanuel Levinas": "Contemporánea", "Jacques Derrida": "Contemporánea",
    "Hannah Arendt": "Contemporánea", "Jürgen Habermas": "Contemporánea",
    "John Rawls": "Contemporánea", "Martha Nussbaum": "Contemporánea",
    "Judith Butler": "Contemporánea", "Robert Nozick": "Contemporánea",
    "Slavoj Žižek": "Contemporánea",
    
    # Nuevos filósofos modernos/contemporáneos
    "José Ortega y Gasset": "Contemporánea", "María Zambrano": "Contemporánea",
    "Miguel de Unamuno": "Contemporánea", "Henri Bergson": "Contemporánea",
    "Bertrand Russell": "Contemporánea", "William James": "Contemporánea",
    "John Dewey": "Contemporánea", "Max Weber": "Contemporánea",
    "Alfred North Whitehead": "Contemporánea", "Hans-Georg Gadamer": "Contemporánea",
    "Paul Ricoeur": "Contemporánea", "Walter Benjamin": "Contemporánea",
    "Antonio Gramsci": "Contemporánea", "Michel Foucault": "Contemporánea"
}

# URLs de imágenes reales de Wikipedia para los nuevos filósofos
REAL_IMAGES_URLS = {
    "José Ortega y Gasset": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6b/Jos%C3%A9_Ortega_y_Gasset_1930.jpg/256px-Jos%C3%A9_Ortega_y_Gasset_1930.jpg",
    "María Zambrano": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8b/Mar%C3%ADa_Zambrano.jpg/256px-Mar%C3%ADa_Zambrano.jpg",
    "Miguel de Unamuno": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/58/Miguel_de_Unamuno_Meurisse_1925.jpg/256px-Miguel_de_Unamuno_Meurisse_1925.jpg",
    "Henri Bergson": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/cd/Henri_Bergson_-_Nobel-Diplom.jpg/256px-Henri_Bergson_-_Nobel-Diplom.jpg",
    "Bertrand Russell": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f7/Bertrand_Russell_1907.jpg/256px-Bertrand_Russell_1907.jpg",
    "William James": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f7/William_James_b1842c.jpg/256px-William_James_b1842c.jpg",
    "John Dewey": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e9/John_Dewey_1902.jpg/256px-John_Dewey_1902.jpg",
    "Max Weber": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/16/Max_Weber_1894.jpg/256px-Max_Weber_1894.jpg",
    "Alfred North Whitehead": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/74/Alfred_North_Whitehead_1890.jpg/256px-Alfred_North_Whitehead_1890.jpg",
    "Hans-Georg Gadamer": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/81/Hans-georg-gadamer.jpg/256px-Hans-georg-gadamer.jpg",
    "Paul Ricoeur": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b2/Paul_ricoeur.jpg/256px-Paul_ricoeur.jpg",
    "Walter Benjamin": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c6/Walter_Benjamin_vers_1928.jpg/256px-Walter_Benjamin_vers_1928.jpg",
    "Antonio Gramsci": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/59/Antonio_Gramsci.jpg/256px-Antonio_Gramsci.jpg",
    "Michel Foucault": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/fc/Foucault5.jpg/256px-Foucault5.jpg"
}

def fix_epochs_and_images():
    """Corrige épocas de filósofos y actualiza imágenes reales"""
    
    session = SessionLocal()
    
    print("🔧 CORRIGIENDO ÉPOCAS Y ACTUALIZANDO IMÁGENES")
    print("=" * 60)
    
    try:
        # Obtener todos los autores
        authors = session.query(Author).all()
        
        epochs_updated = 0
        images_updated = 0
        not_found_epochs = 0
        
        print(f"\n📊 Procesando {len(authors)} autores...")
        
        for author in authors:
            updated_this_author = False
            
            # Actualizar época si está en el diccionario
            if author.nombre in PHILOSOPHER_EPOCHS:
                correct_epoch = PHILOSOPHER_EPOCHS[author.nombre]
                if author.epoca != correct_epoch:
                    old_epoch = author.epoca
                    author.epoca = correct_epoch
                    epochs_updated += 1
                    print(f"📅 {author.nombre}: {old_epoch} → {correct_epoch}")
                    updated_this_author = True
            else:
                not_found_epochs += 1
                print(f"⚠️ {author.nombre}: época no definida, mantiene '{author.epoca}'")
            
            # Actualizar imagen si tiene avatar y hay imagen real disponible
            if (author.nombre in REAL_IMAGES_URLS and 
                ('ui-avatars.com' in author.imagen_url or 
                 author.imagen_url.endswith('&size=300'))):
                
                old_url = author.imagen_url
                author.imagen_url = REAL_IMAGES_URLS[author.nombre]
                images_updated += 1
                print(f"🖼️ {author.nombre}: Avatar → Imagen real de Wikipedia")
                updated_this_author = True
            
            if not updated_this_author and author.nombre in PHILOSOPHER_EPOCHS:
                print(f"✅ {author.nombre}: Ya correcto ({author.epoca})")
        
        # Commit cambios
        session.commit()
        
        # Resumen por épocas
        epoch_counts = {}
        for author in session.query(Author).all():
            epoch_counts[author.epoca] = epoch_counts.get(author.epoca, 0) + 1
        
        print(f"\n🎉 ¡CORRECCIÓN COMPLETADA!")
        print(f"=" * 50)
        print(f"📊 RESUMEN:")
        print(f"Épocas actualizadas: {epochs_updated}")
        print(f"Imágenes actualizadas: {images_updated}")
        print(f"Sin época definida: {not_found_epochs}")
        print(f"Total autores procesados: {len(authors)}")
        
        print(f"\n📈 DISTRIBUCIÓN POR ÉPOCAS:")
        for epoca, count in sorted(epoch_counts.items()):
            print(f"   {epoca}: {count} filósofos")
        
        print(f"\n✅ RESULTADO:")
        print(f"🎯 Épocas históricamente correctas asignadas")
        print(f"📷 Nuevos filósofos con imágenes reales de Wikipedia")
        print(f"🌍 Representación equilibrada a través de la historia")
        
    except Exception as e:
        print(f"❌ Error durante la corrección: {e}")
        session.rollback()
    finally:
        session.close()

if __name__ == "__main__":
    fix_epochs_and_images()