#!/usr/bin/env python3
"""
Script para añadir filósofos modernos y contemporáneos de primera línea que faltan
"""

import os
import sys
sys.path.append('/opt/app')

from app.database import SessionLocal
from app.models import Author, School, Book, Quote
from datetime import date

# Filósofos modernos de primera línea a añadir con biografías detalladas
NEW_MODERN_PHILOSOPHERS = {
    "José Ortega y Gasset": {
        "biografia": "Filósofo español del siglo XX, figura central de la filosofía hispana. Desarrolló el perspectivismo y el concepto de 'razón vital'. Su obra 'La rebelión de las masas' analiza la sociedad de masas moderna. Fundó la Revista de Occidente, crucial para la modernización intelectual de España.",
        "epoca": "Contemporánea",
        "fecha_nacimiento": date(1883, 5, 9),
        "fecha_defuncion": date(1955, 10, 18)
    },
    
    "María Zambrano": {
        "biografia": "Filósofa española discípula de Ortega y Gasset. Desarrolló una filosofía poética que integra razón y corazón. Su 'razón poética' busca superar la crisis de la razón moderna. Exiliada durante el franquismo, es una de las pensadoras más originales del siglo XX.",
        "epoca": "Contemporánea", 
        "fecha_nacimiento": date(1904, 4, 22),
        "fecha_defuncion": date(1991, 2, 6)
    },
    
    "Miguel de Unamuno": {
        "biografia": "Filósofo y escritor español, figura clave de la Generación del 98. Su obra 'Del sentimiento trágico de la vida' explora la tensión entre razón y fe. Desarrolló el concepto de 'intrahistoria' y exploró temas existenciales como la inmortalidad y la agonía del cristianismo.",
        "epoca": "Contemporánea",
        "fecha_nacimiento": date(1864, 9, 29), 
        "fecha_defuncion": date(1936, 12, 31)
    },
    
    "Henri Bergson": {
        "biografia": "Filósofo francés Premio Nobel de Literatura 1927. Desarrolló una filosofía vitalista que enfatiza la intuición sobre el intelecto. Sus obras sobre el tiempo, la memoria y la evolución creadora influyeron profundamente en la filosofía y las artes del siglo XX.",
        "epoca": "Contemporánea",
        "fecha_nacimiento": date(1859, 10, 18),
        "fecha_defuncion": date(1941, 1, 4)
    },
    
    "Bertrand Russell": {
        "biografia": "Filósofo, lógico y matemático británico, Premio Nobel de Literatura 1950. Junto con Whitehead desarrolló los 'Principia Mathematica'. Sus contribuciones a la lógica, filosofía del lenguaje y epistemología fueron fundamentales. También fue activista pacifista y social.",
        "epoca": "Contemporánea",
        "fecha_nacimiento": date(1872, 5, 18),
        "fecha_defuncion": date(1970, 2, 2)
    },
    
    "William James": {
        "biografia": "Filósofo y psicólogo estadounidense, fundador del pragmatismo junto con Pierce y Dewey. Desarrolló el 'empirismo radical' y estudios pioneros sobre experiencia religiosa y conciencia. Su teoría de la verdad como 'lo que funciona' influyó enormemente en la filosofía americana.",
        "epoca": "Contemporánea",
        "fecha_nacimiento": date(1842, 1, 11),
        "fecha_defuncion": date(1910, 8, 26)
    },
    
    "John Dewey": {
        "biografia": "Filósofo estadounidense, principal exponente del pragmatismo. Revolucionó la educación con su filosofía 'aprender haciendo'. Sus trabajos sobre democracia, educación y experiencia lo convierten en una figura fundamental del pensamiento progresista americano.",
        "epoca": "Contemporánea", 
        "fecha_nacimiento": date(1859, 10, 20),
        "fecha_defuncion": date(1952, 6, 1)
    },
    
    "Max Weber": {
        "biografia": "Sociólogo, economista y filósofo alemán, figura fundacional de la sociología moderna. Su 'Ética protestante y el espíritu del capitalismo' es fundamental para entender la modernidad. Desarrolló conceptos como 'tipos ideales', 'desencantamiento del mundo' y análisis de la burocracia.",
        "epoca": "Contemporánea",
        "fecha_nacimiento": date(1864, 4, 21),
        "fecha_defuncion": date(1920, 6, 14)
    },
    
    "Alfred North Whitehead": {
        "biografia": "Matemático y filósofo británico, coautor con Russell de los 'Principia Mathematica'. Desarrolló la 'filosofía del proceso', una metafísica que ve la realidad como constituida por procesos antes que sustancias. Su pensamiento influyó en teología, cosmología y filosofía de la ciencia.",
        "epoca": "Contemporánea",
        "fecha_nacimiento": date(1861, 2, 15),
        "fecha_defuncion": date(1947, 12, 30)
    },
    
    "Hans-Georg Gadamer": {
        "biografia": "Filósofo alemán, principal exponente de la hermenéutica filosófica. Su obra 'Verdad y método' revolucionó la comprensión de la interpretación. Desarrolló conceptos como 'fusión de horizontes' y 'círculo hermenéutico', fundamentales para las ciencias humanas y la filosofía continental.",
        "epoca": "Contemporánea",
        "fecha_nacimiento": date(1900, 2, 11),
        "fecha_defuncion": date(2002, 3, 13)
    },
    
    "Paul Ricoeur": {
        "biografia": "Filósofo francés que integró hermenéutica, fenomenología y estructuralismo. Sus trabajos sobre narratividad, memoria e identidad personal son fundamentales. Desarrolló una 'hermenéutica del sí mismo' y contribuyó significativamente a la filosofía del lenguaje y la ética.",
        "epoca": "Contemporánea",
        "fecha_nacimiento": date(1913, 2, 27),
        "fecha_defuncion": date(2005, 5, 20)
    },
    
    "Walter Benjamin": {
        "biografia": "Filósofo y crítico cultural alemán asociado con la Escuela de Frankfurt. Sus ensayos sobre arte, literatura y cultura moderna, como 'La obra de arte en la época de su reproductibilidad técnica', fueron revolucionarios. Su pensamiento combina marxismo, misticismo judío y crítica estética.",
        "epoca": "Contemporánea",
        "fecha_nacimiento": date(1892, 7, 15),
        "fecha_defuncion": date(1940, 9, 26)
    },
    
    "Antonio Gramsci": {
        "biografia": "Filósofo y teórico político italiano, fundador del Partido Comunista Italiano. Desarrolló conceptos como 'hegemonía cultural' y 'intelectual orgánico'. Sus 'Cuadernos de la cárcel', escritos durante su encarcelamiento fascista, renovaron profundamente la teoría marxista.",
        "epoca": "Contemporánea",
        "fecha_nacimiento": date(1891, 1, 22),
        "fecha_defuncion": date(1937, 4, 27)
    },
    
    "Michel Foucault": {
        "biografia": "Filósofo francés del siglo XX, figura clave del postestructuralismo. Sus análisis sobre poder, saber y sexualidad revolucionaron las ciencias humanas. Obras como 'Historia de la locura', 'Vigilar y castigar' y 'Historia de la sexualidad' influyeron profundamente en filosofía, sociología e historia.",
        "epoca": "Contemporánea",
        "fecha_nacimiento": date(1926, 10, 15),
        "fecha_defuncion": date(1984, 6, 25)
    }
}

def add_modern_philosophers():
    """Añade filósofos modernos de primera línea a la base de datos"""
    
    session = SessionLocal()
    
    print("➕ AÑADIENDO FILÓSOFOS MODERNOS DE PRIMERA LÍNEA")
    print("=" * 60)
    
    try:
        added_count = 0
        already_exists_count = 0
        
        # Obtener una escuela por defecto para asignar
        default_school = session.query(School).first()
        
        for name, data in NEW_MODERN_PHILOSOPHERS.items():
            print(f"\n➕ Procesando {name}...")
            
            # Verificar si ya existe
            existing_author = session.query(Author).filter(Author.nombre == name).first()
            
            if existing_author:
                print(f"⚠️ {name} ya existe en la base de datos")
                already_exists_count += 1
                continue
            
            # Crear nuevo autor
            new_author = Author(
                nombre=name,
                epoca=data["epoca"],
                fecha_nacimiento=data["fecha_nacimiento"],
                fecha_defuncion=data["fecha_defuncion"],
                imagen_url=f"https://ui-avatars.com/api/?name={name.replace(' ', '+')}&background=random&size=300",
                biografia=data["biografia"]
            )
            
            # Asignar escuela por defecto
            if default_school:
                new_author.schools.append(default_school)
            
            session.add(new_author)
            session.flush()  # Para obtener el ID
            
            # Crear libro asociado
            book = Book(
                titulo=f"Obras de {name}",
                imagen_url=f"https://ui-avatars.com/api/?name={name.replace(' ', '+')[:15]}&background=green&color=white&size=200",
                descripcion=f"Recopilación de las principales obras de {name}",
                autor_id=new_author.id
            )
            session.add(book)
            
            # Crear cita asociada
            quote = Quote(
                texto=f"Reflexión filosófica de {name}",
                autor_id=new_author.id
            )
            session.add(quote)
            
            added_count += 1
            print(f"✅ {name}: Añadido exitosamente")
            print(f"   📅 {data['fecha_nacimiento'].year}-{data['fecha_defuncion'].year if data['fecha_defuncion'] else 'presente'}")
            print(f"   📝 {data['biografia'][:80]}...")
        
        # Commit cambios
        session.commit()
        
        # Verificar total final
        total_authors = session.query(Author).count()
        
        print(f"\n🎉 ¡AÑADIDOS FILÓSOFOS MODERNOS!")
        print(f"=" * 50)
        print(f"📊 RESUMEN:")
        print(f"Filósofos añadidos: {added_count}")
        print(f"Ya existían: {already_exists_count}")
        print(f"Total filósofos procesados: {len(NEW_MODERN_PHILOSOPHERS)}")
        print(f"Total autores en la base de datos: {total_authors}")
        
        print(f"\n✅ RESULTADO:")
        print(f"📚 La base ahora incluye los filósofos modernos más importantes")
        print(f"🌍 Representación mejorada de la filosofía hispana, francesa, alemana y anglosajona")
        
    except Exception as e:
        print(f"❌ Error durante la adición: {e}")
        session.rollback()
    finally:
        session.close()

if __name__ == "__main__":
    add_modern_philosophers()