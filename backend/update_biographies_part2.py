#!/usr/bin/env python3
"""
Script para actualizar biografías - Parte 2: Medievales, Modernos y Contemporáneos
"""

import os
import sys
sys.path.append('/opt/app')

from app.database import SessionLocal
from app.models import Author

# Biografías para filósofos medievales, modernos y contemporáneos
BIOGRAPHIES_PART2 = {
    # Medievales Cristianos
    "Tomás de Aquino": "Santo Tomás de Aquino, teólogo y filósofo italiano del siglo XIII. Sintetizó la filosofía aristotélica con la doctrina cristiana en su 'Suma Teológica'. Desarrolló las cinco vías para demostrar la existencia de Dios. Es el principal representante de la escolástica y Doctor de la Iglesia.",
    
    "San Agustín": "Aurelio Agustín de Hipona, teólogo y filósofo cristiano del siglo IV-V. Sus 'Confesiones' son pioneras del género autobiográfico. En 'La Ciudad de Dios' desarrolla una filosofía cristiana de la historia. Sintetizó cristianismo y platonismo, influyendo en toda la filosofía medieval.",
    
    "Anselmo de Canterbury": "Santo Anselmo, filósofo y teólogo benedictino del siglo XI. Famoso por su argumento ontológico para demostrar la existencia de Dios: Dios es 'aquello mayor que lo cual nada puede pensarse'. Desarrolló el principio 'fides quaerens intellectum' (la fe busca el entendimiento).",
    
    "Pedro Abelardo": "Filósofo y teólogo francés del siglo XII. Desarrolló la dialéctica como método teológico. Su correspondencia amorosa con Eloísa es famosa en la literatura. Propuso el conceptualismo como solución al problema de los universales.",
    
    "Juan Escoto Erígena": "Filósofo irlandés del siglo IX, traductor de Dionisio Areopagita. Su 'División de la Naturaleza' presenta una síntesis neoplatónica única en el pensamiento medieval. Influyó en el misticismo posterior y fue controversial por sus ideas sobre la predestinación.",
    
    "Boecio": "Anicio Manlio Severino Boecio, filósofo romano del siglo VI. Su 'Consolación de la Filosofía', escrita en prisión, es una de las obras más influyentes del pensamiento medieval. Tradujo y comentó a Aristóteles, siendo un puente entre la filosofía antigua y medieval.",
    
    "Alberto Magno": "San Alberto Magno, filósofo y científico alemán del siglo XIII. Maestro de Tomás de Aquino, introdujo el aristotelismo en el mundo cristiano. Hizo importantes contribuciones a las ciencias naturales y fue pionero en el estudio empírico de la naturaleza.",
    
    "Buenaventura": "San Buenaventura de Bagnoregio, franciscano y teólogo del siglo XIII. Desarrolló una síntesis entre agustinismo y aristotelismo. Su 'Itinerario de la mente hacia Dios' es una obra mística fundamental. Defendió la iluminación divina como fuente del conocimiento.",
    
    "Meister Eckhart": "Johannes Eckhart, místico y teólogo dominico alemán del siglo XIII-XIV. Sus sermones en alemán vulgar influyeron profundamente en la mística renana. Desarrolló conceptos como 'desapego' y la 'chispa del alma'. Influyó en Tauler, Suso y la mística posterior.",
    
    "Duns Escoto": "Juan Duns Escoto, franciscano y teólogo escocés del siglo XIII-XIV. Desarrolló el 'escotismo' como alternativa al tomismo. Famoso por su defensa de la Inmaculada Concepción y por el concepto de 'haecceitas' (unicidad individual).",
    
    "Guillermo de Ockham": "Franciscano inglés del siglo XIV, famoso por la 'navaja de Ockham': no multiplicar los entes sin necesidad. Desarrolló el nominalismo extremo y contribuyó a la lógica medieval. Sus ideas políticas sobre la separación de poderes influyeron en el pensamiento moderno.",
    
    # Filosofía Oriental
    "Confucio": "Kong Qiu, pensador chino del siglo VI-V a.C. Sus enseñanzas, recopiladas en las 'Analectas', enfatizan la moralidad personal, la rectitud en las relaciones sociales y la justicia. El confucianismo se convirtió en la doctrina oficial del Estado chino durante siglos.",
    
    "Lao Tzu": "Legendario fundador del taoísmo en el siglo VI a.C. El 'Tao Te Ching' que se le atribuye es fundamental para entender el taoísmo. Enseña sobre el Tao (el Camino), el wu wei (no-acción) y la armonía con la naturaleza.",
    
    "Buda": "Siddhartha Gautama, fundador del budismo en el siglo VI-V a.C. Tras alcanzar la iluminación bajo el árbol Bodhi, enseñó las Cuatro Nobles Verdades y el Óctuple Sendero como camino para superar el sufrimiento y alcanzar el Nirvana.",
    
    "Nagarjuna": "Filósofo budista indio del siglo II d.C., fundador de la escuela Madhyamaka (Camino Medio). Desarrolló la doctrina de la 'vacuidad' (sunyata), argumentando que todos los fenómenos carecen de existencia inherente.",
    
    "Mencio": "Meng Zi, filósofo confuciano chino del siglo IV a.C. Desarrolló la teoría de que la naturaleza humana es intrínsecamente buena. Sus ideas sobre la benevolencia gubernamental y la rectificación moral influyeron profundamente en el confucianismo posterior.",
    
    "Zhuangzi": "Zhuang Zhou, filósofo taoísta chino del siglo IV a.C. Sus escritos, llenos de paradojas y alegorías, desarrollan temas como la relatividad de todas las cosas, la transformación constante y la libertad espiritual. Influyó en el budismo zen.",
    
    "Xunzi": "Xun Kuang, filósofo confuciano del siglo III a.C. En contraste con Mencio, argumentó que la naturaleza humana es intrínsecamente mala y debe ser corregida mediante rituales y educación. Influyó en el legalismo chino.",
    
    "Mozi": "Mo Di, filósofo chino del siglo V a.C., fundador del mohismo. Predicaba el 'amor universal' sin distinciones y la 'utilidad mutua'. Se oponía tanto al confucianismo como al taoísmo, promoviendo una ética basada en las consecuencias.",
    
    "Shankara": "Adi Shankara, filósofo y místico hindú del siglo VIII d.C. Principal exponente del Advaita Vedanta, que enseña la no-dualidad entre el alma individual (Atman) y la realidad absoluta (Brahman). Sistematizó la filosofía vedántica.",
    
    # Filósofos Modernos
    "René Descartes": "Filósofo y matemático francés del siglo XVII, considerado padre de la filosofía moderna. Su método de duda sistemática lo llevó al 'cogito ergo sum' (pienso, luego existo). Estableció el dualismo mente-cuerpo y revolucionó tanto filosofía como matemáticas.",
    
    "Baruch Spinoza": "Filósofo holandés del siglo XVII. Su 'Ética' presenta un sistema filosófico geométrico donde Dios y la Naturaleza son idénticos. Defendió el determinismo absoluto y una ética basada en el conocimiento racional. Fue excomulgado de la comunidad judía por sus ideas.",
    
    "John Locke": "Filósofo inglés del siglo XVII, padre del empirismo moderno y del liberalismo político. Su 'Ensayo sobre el entendimiento humano' niega las ideas innatas. Sus 'Dos tratados sobre el gobierno civil' influyeron en las revoluciones americana y francesa.",
    
    "David Hume": "Filósofo escocés del siglo XVIII, figura clave del empirismo y la Ilustración escocesa. Su escepticismo sobre la causalidad y la inducción despertó a Kant de su 'sueño dogmático'. Escribió importantes trabajos sobre religión, moral e historia.",
    
    "Immanuel Kant": "Filósofo alemán del siglo XVIII, figura central de la filosofía moderna. Su 'Crítica de la razón pura' sintetiza racionalismo y empirismo. Desarrolló la ética del deber categórico y la idea de la 'paz perpetua'. Revolucionó metafísica, epistemología y ética.",
    
    "Georg Hegel": "Filósofo alemán del siglo XIX. Su sistema dialéctico comprende toda la realidad como desarrollo del Espíritu Absoluto a través de tesis, antítesis y síntesis. Su filosofía de la historia y del Estado influyó profundamente en el pensamiento posterior.",
    
    "Friedrich Nietzsche": "Filósofo alemán del siglo XIX. Proclamó la 'muerte de Dios' y desarrolló conceptos como el 'superhombre', la 'voluntad de poder' y el 'eterno retorno'. Su crítica de la moral occidental y su estilo aforístico influyeron enormemente en el pensamiento contemporáneo.",
    
    "Søren Kierkegaard": "Filósofo y teólogo danés del siglo XIX, considerado precursor del existencialismo. Exploró temas como la angustia, la elección, la fe y la existencia individual. Sus 'estadios en el camino de la vida' describen el desarrollo espiritual humano.",
    
    "Arthur Schopenhauer": "Filósofo alemán del siglo XIX. Su obra principal 'El mundo como voluntad y representación' presenta un pesimismo metafísico donde la voluntad ciega es la esencia del mundo. Influyó en Nietzsche, Wagner y el pensamiento oriental en Occidente.",
    
    "Karl Marx": "Filósofo, economista y revolucionario alemán del siglo XIX. Desarrolló el materialismo histórico y la crítica de la economía política capitalista. Su análisis de la lucha de clases y la alienación influyó profundamente en la política y filosofía del siglo XX.",
    
    "Ludwig Wittgenstein": "Filósofo austro-británico del siglo XX. Su 'Tractus Logico-Philosophicus' influyó en el positivismo lógico. Posteriormente, sus 'Investigaciones filosóficas' revolucionaron la filosofía del lenguaje con la teoría de los 'juegos del lenguaje'.",
    
    "Martin Heidegger": "Filósofo alemán del siglo XX. Su análisis del 'Dasein' (ser-ahí) en 'Ser y tiempo' renovó la ontología fundamental. Exploró temas como la autenticidad, la angustia ante la muerte y el olvido del ser en la metafísica occidental.",
    
    "Jean-Paul Sartre": "Filósofo francés del siglo XX, figura principal del existencialismo. Su máxima 'la existencia precede a la esencia' enfatiza la libertad y responsabilidad humanas. También fue novelista, dramaturgo y activista político comprometido.",
    
    "Simone de Beauvoir": "Filósofa francesa del siglo XX, pionera del feminismo moderno. Su obra 'El segundo sexo' analiza la construcción social de la feminidad y la opresión de la mujer. También desarrolló importantes contribuciones al existencialismo.",
    
    "Edmund Husserl": "Filósofo alemán fundador de la fenomenología. Desarrolló el método fenomenológico para estudiar la conciencia y sus estructuras intencionales. Su lema 'a las cosas mismas' influyó en toda la filosofía continental del siglo XX.",
    
    "Maurice Merleau-Ponty": "Filósofo francés del siglo XX que desarrolló la fenomenología de la percepción. Enfatizó la importancia del cuerpo vivido en la experiencia y criticó el dualismo cartesiano. Influyó en la psicología cognitiva y las ciencias cognitivas.",
    
    "Emmanuel Levinas": "Filósofo lituano-francés del siglo XX. Desarrolló una ética basada en la responsabilidad hacia el 'Otro' que antecede a la ontología. Su pensamiento sobre la alteridad influyó profundamente en la filosofía contemporánea y la teología.",
    
    "Jacques Derrida": "Filósofo francés del siglo XX, fundador de la deconstrucción. Criticó la tradición logocéntrica occidental y desarrolló conceptos como 'différance' y 'escritura'. Su trabajo influyó en literatura, derecho, arquitectura y estudios culturales.",
    
    "Hannah Arendt": "Filósofa política alemana-estadounidense del siglo XX. Analizó el totalitarismo, la naturaleza del poder y la condición humana. Su concepto de 'banalidad del mal' y su distinción entre labor, trabajo y acción influyeron en la teoría política contemporánea.",
    
    "Jürgen Habermas": "Filósofo y sociólogo alemán contemporáneo. Desarrolló la teoría de la acción comunicativa y la ética del discurso. Sus trabajos sobre la esfera pública, la modernidad y la razón comunicativa son fundamentales en la filosofía política actual.",
    
    "John Rawls": "Filósofo político estadounidense del siglo XX. Su 'Teoría de la Justicia' revitalizó la filosofía política con la teoría de la 'posición original' y el 'velo de la ignorancia' para determinar principios justos de organización social.",
    
    "Robert Nozick": "Filósofo político estadounidense del siglo XX. Su 'Anarquía, Estado y Utopía' presenta una defensa libertaria del Estado mínimo y crítica las teorías redistributivas de la justicia, especialmente la de Rawls.",
    
    "Martha Nussbaum": "Filósofa estadounidense contemporánea especializada en filosofía moral y política. Ha desarrollado importantes trabajos sobre las emociones, las capacidades humanas, el cosmopolitismo y el feminismo desde una perspectiva aristotélica.",
    
    "Judith Butler": "Filósofa estadounidense contemporánea, figura clave en los estudios de género. Su teoría de la performatividad del género ha sido fundamental para entender cómo se construyen socialmente las identidades de género y sexuales.",
    
    "Slavoj Žižek": "Filósofo esloveno contemporáneo que combina psicoanálisis lacaniano, marxismo y crítica cultural. Sus análisis de la ideología y la cultura popular han hecho accesible la teoría crítica a audiencias amplias."
}

def update_biographies_part2():
    """Actualiza las biografías de filósofos medievales, modernos y contemporáneos"""
    
    session = SessionLocal()
    
    print("📚 ACTUALIZANDO BIOGRAFÍAS - PARTE 2")
    print("=" * 50)
    
    try:
        updated_count = 0
        not_found_count = 0
        
        for name, biography in BIOGRAPHIES_PART2.items():
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
            print(f"   Nueva: {biography[:80]}...")
        
        # Commit cambios
        session.commit()
        
        print(f"\n🎉 ¡ACTUALIZACIÓN PARTE 2 COMPLETADA!")
        print(f"📊 Biografías actualizadas: {updated_count}")
        print(f"❌ Autores no encontrados: {not_found_count}")
        print(f"📈 Total biografías actualizadas en parte 2: {updated_count}")
        
    except Exception as e:
        print(f"❌ Error durante la actualización: {e}")
        session.rollback()
    finally:
        session.close()

if __name__ == "__main__":
    update_biographies_part2()