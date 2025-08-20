#!/usr/bin/env python3
"""
Script para actualizar las biografías de filósofos con contenido real y detallado
"""

import os
import sys
sys.path.append('/opt/app')

from app.database import SessionLocal
from app.models import Author

# Biografías detalladas para cada filósofo
BIOGRAPHIES = {
    "Sócrates": "Filósofo griego considerado el fundador de la filosofía occidental. Desarrolló el método socrático de investigación basado en preguntas. No escribió ningún texto, conocemos su pensamiento através de Platón. Fue condenado a muerte por corromper a la juventud y no creer en los dioses de la ciudad.",
    
    "Platón": "Discípulo de Sócrates y maestro de Aristóteles. Fundó la Academia en Atenas. Su filosofía se centra en la teoría de las Ideas o Formas, mundos perfectos e inmutables que trascienden la realidad sensible. Escribió numerosos diálogos donde Sócrates es el personaje principal.",
    
    "Aristóteles": "Filósofo griego discípulo de Platón. Fundó el Liceo y desarrolló un sistema filosófico completo que abarca lógica, ética, política, metafísica y ciencias naturales. Fue tutor de Alejandro Magno. Su influencia se extendió por siglos en el pensamiento occidental.",
    
    "Epicuro": "Filósofo griego fundador del epicureísmo. Propuso que el objetivo de la vida humana es alcanzar la felicidad y evitar el dolor. Distinguió entre placeres necesarios e innecesarios. Fundó el Jardín, una comunidad filosófica que incluía mujeres y esclavos.",
    
    "Zenón de Citio": "Fundador del estoicismo en Atenas. Enseñaba en el Pórtico Pintado (Stoa Poikile). Los estoicos creían en vivir de acuerdo con la naturaleza y aceptar lo que no podemos cambiar, desarrollando virtudes como la sabiduría, justicia, fortaleza y templanza.",
    
    "Pitágoras": "Filósofo y matemático griego famoso por el teorema que lleva su nombre. Fundó una escuela filosófico-religiosa que creía en la transmigración de las almas y en que los números son la esencia de todas las cosas. Influyó profundamente en Platón.",
    
    "Heráclito": "Filósofo presocrático conocido como 'el Oscuro' por su estilo enigmático. Famoso por su doctrina del flujo constante ('no puedes bañarte dos veces en el mismo río') y la unidad de los opuestos. Consideraba el fuego como el elemento primordial.",
    
    "Parménides": "Filósofo presocrático que defendió la inmutabilidad del ser. En su poema 'Sobre la naturaleza' distingue entre el camino de la verdad y el de la opinión. Influyó profundamente en Platón y en toda la metafísica occidental posterior.",
    
    "Séneca": "Filósofo estoico romano, dramaturgo y político. Fue preceptor y consejero del emperador Nerón. Sus 'Cartas a Lucilio' y tratados morales son fundamentales del estoicismo. Defendió la ética práctica y la autosuficiencia moral.",
    
    "Marco Aurelio": "Emperador romano y filósofo estoico. Sus 'Meditaciones', escritas para sí mismo, son una de las obras más importantes del estoicismo tardío. Combinó poder político con sabiduría filosófica, siendo considerado el último de los 'cinco buenos emperadores'.",
    
    "Empédocles": "Filósofo presocrático que propuso la teoría de los cuatro elementos (tierra, agua, aire, fuego) movidos por dos fuerzas: Amor y Discordia. También desarrolló una teoría primitiva de la evolución y fue considerado mago y curandero.",
    
    "Anaxágoras": "Filósofo presocrático que introdujo el concepto de 'nous' (mente) como principio ordenador del cosmos. Fue el primer filósofo en explicar correctamente los eclipses. Maestro de Pericles, fue acusado de impiedady desterrado de Atenas.",
    
    "Demócrito": "Filósofo griego conocido como el 'filósofo que ríe'. Junto con Leucipo, desarrolló la teoría atomista: todo está compuesto de átomos indivisibles que se mueven en el vacío. Su ética se basaba en la moderación y la alegría.",
    
    "Epicteto": "Filósofo estoico nacido esclavo que se convirtió en uno de los maestros más influyentes del estoicismo tardío. Sus 'Discursos' y el 'Manual' (Enquiridión) enseñan la importancia de distinguir entre lo que depende de nosotros y lo que no.",
    
    "Tales de Mileto": "Considerado el primer filósofo occidental. Propuso que el agua es el principio de todas las cosas. Fue también matemático y astrónomo, prediciendo un eclipse solar. Uno de los Siete Sabios de Grecia.",
    
    "Anaximandro": "Discípulo de Tales, propuso el 'ápeiron' (lo indefinido) como principio de todas las cosas. Creó el primer mapa del mundo conocido y desarrolló una teoría evolutiva primitiva. Introdujo el gnomon (reloj de sol) en Grecia.",
    
    "Anaxímenes": "Último de los filósofos de Mileto, propuso el aire como principio fundamental. Desarrolló una teoría de los cambios de estado de la materia por condensación y rarefacción. Influyó en las cosmogonías posteriores.",
    
    "Jenófanes": "Filósofo presocrático que criticó el antropomorfismo de los dioses tradicionales griegos. Propuso un dios único, inmóvil y sin forma humana. También desarrolló ideas sobre el conocimiento y la naturaleza de la investigación.",
    
    "Protágoras": "Sofista griego famoso por la máxima 'el hombre es la medida de todas las cosas'. Desarrolló el relativismo epistemológico y fue uno de los primeros en cobrar por enseñar. Influyó en la democracia ateniense.",
    
    "Gorgias": "Sofista y retórico griego conocido por su nihilismo epistemológico: 'nada existe, si algo existiera no podría ser conocido, y si pudiera ser conocido no podría ser comunicado'. Maestro de la oratoria y la persuasión.",
    
    "Antístenes": "Discípulo de Sócrates y fundador del cinismo. Predicaba la autosuficiencia, la vida simple y el desprecio por las convenciones sociales. Maestro de Diógenes de Sinope. Escribió numerosos diálogos socráticos.",
    
    "Cleantes": "Segundo director de la escuela estoica tras Zenón. Trabajaba como boxeador nocturno para financiar sus estudios filosóficos. Autor del famoso 'Himno a Zeus' donde identifica a Zeus con el logos divino que gobierna el universo.",
    
    "Crisipo": "Tercer director de la Stoa, llamado el 'segundo fundador' del estoicismo por sistematizar la doctrina. Escribió más de 700 obras. Desarrolló la lógica estoica y perfeccionó la teoría del determinismo compatible con la responsabilidad moral.",
    
    "Plotino": "Fundador del neoplatonismo. Su filosofía se centra en la existencia de tres hipóstasis: el Uno, el Intelecto y el Alma. Sus 'Enéadas' influyeron profundamente en el cristianismo y en toda la filosofía posterior hasta el Renacimiento.",
    
    "Proclo": "Último gran filósofo neoplatónico. Dirigió la Academia platónica en sus últimos años. Desarrolló una compleja teología filosófica que influyó en el pensamiento bizantino e islámico. Autor de comentarios fundamentales sobre Platón.",
    
    "Jámblico": "Filósofo neoplatónico que introdujo la teúrgia (práctica ritual) en el platonismo. Sistematizó la filosofía pitagórica y desarrolló una compleja jerarquía de seres divinos. Influyó en el emperador Juliano el Apóstata.",
    
    "Porfirio": "Discípulo de Plotino y editor de las 'Enéadas'. Escribió 'Vida de Plotino' e 'Introducción a las Categorías', texto fundamental para el estudio de la lógica durante siglos. También escribió contra el cristianismo.",
    
    "Simplicio": "Último filósofo de la Academia antes de su cierre por Justiniano. Sus comentarios a Aristóteles son fuentes fundamentales para conocer la filosofía presocrática. Defendió el paganismo intelectual frente al cristianismo.",
    
    "Alejandro de Afrodisias": "El más famoso comentarista de Aristóteles en la Antigüedad tardía. Sus comentarios influyeron enormemente en el aristotelismo medieval islámico y cristiano. Desarrolló interpretaciones materialistas de la psicología aristotélica.",
    
    "Filón de Alejandría": "Filósofo judío helenístico que intentó reconciliar la filosofía griega con la religión judía. Desarrolló el método alegórico de interpretación bíblica. Influyó profundamente en los Padres de la Iglesia cristianos.",
    
    "Diógenes Laercio": "Biógrafo de los filósofos antiguos. Su 'Vidas de los filósofos más ilustres' es una fuente fundamental para conocer la filosofía antigua. Aunque no era filósofo original, preservó información invaluable sobre pensadores perdidos.",
    
    "Apolodoro": "Cronógrafo y mitógrafo griego. Escribió una 'Crónica' que estableció cronologías precisas de eventos históricos y una 'Biblioteca' que sistematizó la mitología griega. Sus trabajos fueron fundamentales para la historiografía antigua.",
    
    "Hierocles": "Filósofo estoico del siglo II d.C. Sus 'Elementos de ética' son una introducción sistemática a la moral estoica. Desarrolló la teoría de la 'oikeiosis' (apropiación) como base del desarrollo moral humano.",
    
    "Luciano de Samósata": "Escritor satírico que ridiculizó las escuelas filosóficas de su época. Sus diálogos humorísticos, como 'Subasta de vidas' y 'Los filósofos a sueldo', ofrecen críticas mordaces del mundo intelectual del siglo II d.C.",
    
    "Galeno": "Médico, cirujano y filósofo griego. Sus tratados médicos dominaron la medicina occidental durante más de mil años. También escribió sobre lógica y filosofía natural, siguiendo principalmente a Aristóteles y los estoicos.",
    
    "Ptolomeo": "Astrónomo, matemático y geógrafo que también escribió sobre filosofía natural. Su 'Almagesto' fue el texto astronómico fundamental hasta Copérnico. Su sistema geocéntrico influyó en la cosmología medieval.",
    
    "Apolonio de Tiana": "Filósofo neopitagórico del siglo I d.C., famoso por sus supuestos poderes milagrosos. Viajó extensamente enseñando una filosofía que combinaba pitagorismo y ascetismo oriental. Su biografía por Filóstrato influyó en las vidas de santos cristianos.",
    
    "Máximo de Tiro": "Filósofo platónico del siglo II d.C. Sus 'Disertaciones' combinan platonismo con elementos estoicos y cínicos. Popular conferenciante que adaptaba la filosofía para audiencias cultas pero no especializadas."
}

def update_biographies():
    """Actualiza las biografías de los filósofos con contenido real"""
    
    session = SessionLocal()
    
    print("📚 ACTUALIZANDO BIOGRAFÍAS DE FILÓSOFOS")
    print("=" * 50)
    
    try:
        updated_count = 0
        not_found_count = 0
        
        for name, biography in BIOGRAPHIES.items():
            print(f"\n📖 Actualizando {name}...")
            
            # Buscar el autor en la base de datos
            author = session.query(Author).filter(Author.nombre == name).first()
            
            if not author:
                print(f"❌ {name} no encontrado en la base de datos")
                not_found_count += 1
                continue
            
            # Actualizar biografía
            old_bio = author.biografia
            author.biografia = biography
            updated_count += 1
            
            print(f"✅ {name}: Biografía actualizada")
            print(f"   Antigua: {old_bio[:50]}...")
            print(f"   Nueva: {biography[:50]}...")
        
        # Commit cambios
        session.commit()
        
        print(f"\n🎉 ¡ACTUALIZACIÓN COMPLETADA!")
        print(f"📊 Biografías actualizadas: {updated_count}")
        print(f"❌ Autores no encontrados: {not_found_count}")
        print(f"📈 Total autores con biografías reales: {updated_count}")
        
    except Exception as e:
        print(f"❌ Error durante la actualización: {e}")
        session.rollback()
    finally:
        session.close()

if __name__ == "__main__":
    update_biographies()