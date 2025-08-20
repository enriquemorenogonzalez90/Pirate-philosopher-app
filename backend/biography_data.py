#!/usr/bin/env python3
"""
Módulo con biografías detalladas para usar en seed.py
"""

def get_author_biography(name: str) -> str:
    """Devuelve una biografía detallada para el autor o una biografía genérica"""
    
    DETAILED_BIOGRAPHIES = {
        # Filósofos Griegos Clásicos
        "Sócrates": "Filósofo griego considerado el fundador de la filosofía occidental. Desarrolló el método socrático de investigación basado en preguntas. No escribió ningún texto, conocemos su pensamiento através de Platón. Fue condenado a muerte por corromper a la juventud y no creer en los dioses de la ciudad.",
        
        "Platón": "Discípulo de Sócrates y maestro de Aristóteles. Fundó la Academia en Atenas. Su filosofía se centra en la teoría de las Ideas o Formas, mundos perfectos e inmutables que trascienden la realidad sensible. Escribió numerosos diálogos donde Sócrates es el personaje principal.",
        
        "Aristóteles": "Filósofo griego discípulo de Platón. Fundó el Liceo y desarrolló un sistema filosófico completo que abarca lógica, ética, política, metafísica y ciencias naturales. Fue tutor de Alejandro Magno. Su influencia se extendió por siglos en el pensamiento occidental.",
        
        "Epicuro": "Filósofo griego fundador del epicureísmo. Propuso que el objetivo de la vida humana es alcanzar la felicidad y evitar el dolor. Distinguió entre placeres necesarios e innecesarios. Fundó el Jardín, una comunidad filosófica que incluía mujeres y esclavos.",
        
        "Zenón de Citio": "Fundador del estoicismo en Atenas. Enseñaba en el Pórtico Pintado (Stoa Poikile). Los estoicos creían en vivir de acuerdo con la naturaleza y aceptar lo que no podemos cambiar, desarrollando virtudes como la sabiduría, justicia, fortaleza y templanza.",
        
        "Pitágoras": "Filósofo y matemático griego famoso por el teorema que lleva su nombre. Fundó una escuela filosófico-religiosa que creía en la transmigración de las almas y en que los números son la esencia de todas las cosas. Influyó profundamente en Platón.",
        
        "Heráclito": "Filósofo presocrático conocido como 'el Oscuro' por su estilo enigmático. Famoso por su doctrina del flujo constante ('no puedes bañarte dos veces en el mismo río') y la unidad de los opuestos. Consideraba el fuego como el elemento primordial.",
        
        "Parménides": "Filósofo presocrático que defendió la inmutabilidad del ser. En su poema 'Sobre la naturaleza' distingue entre el camino de la verdad y el de la opinión. Influyó profundamente en Platón y en toda la metafísica occidental posterior.",
        
        # Estoicos Romanos
        "Séneca": "Filósofo estoico romano, dramaturgo y político. Fue preceptor y consejero del emperador Nerón. Sus 'Cartas a Lucilio' y tratados morales son fundamentales del estoicismo. Defendió la ética práctica y la autosuficiencia moral.",
        
        "Marco Aurelio": "Emperador romano y filósofo estoico. Sus 'Meditaciones', escritas para sí mismo, son una de las obras más importantes del estoicismo tardío. Combinó poder político con sabiduría filosófica, siendo considerado el último de los 'cinco buenos emperadores'.",
        
        "Epicteto": "Filósofo estoico nacido esclavo que se convirtió en uno de los maestros más influyentes del estoicismo tardío. Sus 'Discursos' y el 'Manual' (Enquiridión) enseñan la importancia de distinguir entre lo que depende de nosotros y lo que no.",
        
        # Filósofos Medievales
        "Tomás de Aquino": "Santo Tomás de Aquino, teólogo y filósofo italiano del siglo XIII. Sintetizó la filosofía aristotélica con la doctrina cristiana en su 'Suma Teológica'. Desarrolló las cinco vías para demostrar la existencia de Dios. Es el principal representante de la escolástica y Doctor de la Iglesia.",
        
        "San Agustín": "Aurelio Agustín de Hipona, teólogo y filósofo cristiano del siglo IV-V. Sus 'Confesiones' son pioneras del género autobiográfico. En 'La Ciudad de Dios' desarrolla una filosofía cristiana de la historia. Sintetizó cristianismo y platonismo, influyendo en toda la filosofía medieval.",
        
        # Filosofía Oriental
        "Confucio": "Kong Qiu, pensador chino del siglo VI-V a.C. Sus enseñanzas, recopiladas en las 'Analectas', enfatizan la moralidad personal, la rectitud en las relaciones sociales y la justicia. El confucianismo se convirtió en la doctrina oficial del Estado chino durante siglos.",
        
        "Lao Tzu": "Legendario fundador del taoísmo en el siglo VI a.C. El 'Tao Te Ching' que se le atribuye es fundamental para entender el taoísmo. Enseña sobre el Tao (el Camino), el wu wei (no-acción) y la armonía con la naturaleza.",
        
        "Buda": "Siddhartha Gautama, fundador del budismo en el siglo VI-V a.C. Tras alcanzar la iluminación bajo el árbol Bodhi, enseñó las Cuatro Nobles Verdades y el Óctuple Sendero como camino para superar el sufrimiento y alcanzar el Nirvana.",
        
        # Filósofos Modernos
        "René Descartes": "Filósofo y matemático francés del siglo XVII, considerado padre de la filosofía moderna. Su método de duda sistemática lo llevó al 'cogito ergo sum' (pienso, luego existo). Estableció el dualismo mente-cuerpo y revolucionó tanto filosofía como matemáticas.",
        
        "Baruch Spinoza": "Filósofo holandés del siglo XVII. Su 'Ética' presenta un sistema filosófico geométrico donde Dios y la Naturaleza son idénticos. Defendió el determinismo absoluto y una ética basada en el conocimiento racional. Fue excomulgado de la comunidad judía por sus ideas.",
        
        "John Locke": "Filósofo inglés del siglo XVII, padre del empirismo moderno y del liberalismo político. Su 'Ensayo sobre el entendimiento humano' niega las ideas innatas. Sus 'Dos tratados sobre el gobierno civil' influyeron en las revoluciones americana y francesa.",
        
        "David Hume": "Filósofo escocés del siglo XVIII, figura clave del empirismo y la Ilustración escocesa. Su escepticismo sobre la causalidad y la inducción despertó a Kant de su 'sueño dogmático'. Escribió importantes trabajos sobre religión, moral e historia.",
        
        "Immanuel Kant": "Filósofo alemán del siglo XVIII, figura central de la filosofía moderna. Su 'Crítica de la razón pura' sintetiza racionalismo y empirismo. Desarrolló la ética del deber categórico y la idea de la 'paz perpetua'. Revolucionó metafísica, epistemología y ética.",
        
        "Georg Hegel": "Filósofo alemán del siglo XIX. Su sistema dialéctico comprende toda la realidad como desarrollo del Espíritu Absoluto a través de tesis, antítesis y síntesis. Su filosofía de la historia y del Estado influyó profundamente en el pensamiento posterior.",
        
        "Friedrich Nietzsche": "Filósofo alemán del siglo XIX. Proclamó la 'muerte de Dios' y desarrolló conceptos como el 'superhombre', la 'voluntad de poder' y el 'eterno retorno'. Su crítica de la moral occidental y su estilo aforístico influyeron enormemente en el pensamiento contemporáneo.",
        
        "Karl Marx": "Filósofo, economista y revolucionario alemán del siglo XIX. Desarrolló el materialismo histórico y la crítica de la economía política capitalista. Su análisis de la lucha de clases y la alienación influyó profundamente en la política y filosofía del siglo XX.",
        
        # Filósofos Contemporáneos  
        "Ludwig Wittgenstein": "Filósofo austro-británico del siglo XX. Su 'Tractus Logico-Philosophicus' influyó en el positivismo lógico. Posteriormente, sus 'Investigaciones filosóficas' revolucionaron la filosofía del lenguaje con la teoría de los 'juegos del lenguaje'.",
        
        "Jean-Paul Sartre": "Filósofo francés del siglo XX, figura principal del existencialismo. Su máxima 'la existencia precede a la esencia' enfatiza la libertad y responsabilidad humanas. También fue novelista, dramaturgo y activista político comprometido.",
        
        "Simone de Beauvoir": "Filósofa francesa del siglo XX, pionera del feminismo moderno. Su obra 'El segundo sexo' analiza la construcción social de la feminidad y la opresión de la mujer. También desarrolló importantes contribuciones al existencialismo.",
        
        "Hannah Arendt": "Filósofa política alemana-estadounidense del siglo XX. Analizó el totalitarismo, la naturaleza del poder y la condición humana. Su concepto de 'banalidad del mal' y su distinción entre labor, trabajo y acción influyeron en la teoría política contemporánea.",
        
        # Filósofos Modernos y Contemporáneos añadidos
        "José Ortega y Gasset": "Filósofo español del siglo XX, figura central de la filosofía hispana. Desarrolló el perspectivismo y el concepto de 'razón vital'. Su obra 'La rebelión de las masas' analiza la sociedad de masas moderna. Fundó la Revista de Occidente, crucial para la modernización intelectual de España.",
        
        "María Zambrano": "Filósofa española discípula de Ortega y Gasset. Desarrolló una filosofía poética que integra razón y corazón. Su 'razón poética' busca superar la crisis de la razón moderna. Exiliada durante el franquismo, es una de las pensadoras más originales del siglo XX.",
        
        "Miguel de Unamuno": "Filósofo y escritor español, figura clave de la Generación del 98. Su obra 'Del sentimiento trágico de la vida' explora la tensión entre razón y fe. Desarrolló el concepto de 'intrahistoria' y exploró temas existenciales como la inmortalidad y la agonía del cristianismo.",
        
        "Henri Bergson": "Filósofo francés Premio Nobel de Literatura 1927. Desarrolló una filosofía vitalista que enfatiza la intuición sobre el intelecto. Sus obras sobre el tiempo, la memoria y la evolución creadora influyeron profundamente en la filosofía y las artes del siglo XX.",
        
        "Bertrand Russell": "Filósofo, lógico y matemático británico, Premio Nobel de Literatura 1950. Junto con Whitehead desarrolló los 'Principia Mathematica'. Sus contribuciones a la lógica, filosofía del lenguaje y epistemología fueron fundamentales. También fue activista pacifista y social.",
        
        "William James": "Filósofo y psicólogo estadounidense, fundador del pragmatismo junto con Pierce y Dewey. Desarrolló el 'empirismo radical' y estudios pioneros sobre experiencia religiosa y conciencia. Su teoría de la verdad como 'lo que funciona' influyó enormemente en la filosofía americana.",
        
        "John Dewey": "Filósofo estadounidense, principal exponente del pragmatismo. Revolucionó la educación con su filosofía 'aprender haciendo'. Sus trabajos sobre democracia, educación y experiencia lo convierten en una figura fundamental del pensamiento progresista americano.",
        
        "Max Weber": "Sociólogo, economista y filósofo alemán, figura fundacional de la sociología moderna. Su 'Ética protestante y el espíritu del capitalismo' es fundamental para entender la modernidad. Desarrolló conceptos como 'tipos ideales', 'desencantamiento del mundo' y análisis de la burocracia.",
        
        "Alfred North Whitehead": "Matemático y filósofo británico, coautor con Russell de los 'Principia Mathematica'. Desarrolló la 'filosofía del proceso', una metafísica que ve la realidad como constituida por procesos antes que sustancias. Su pensamiento influyó en teología, cosmología y filosofía de la ciencia.",
        
        "Hans-Georg Gadamer": "Filósofo alemán, principal exponente de la hermenéutica filosófica. Su obra 'Verdad y método' revolucionó la comprensión de la interpretación. Desarrolló conceptos como 'fusión de horizontes' y 'círculo hermenéutico', fundamentales para las ciencias humanas y la filosofía continental.",
        
        "Paul Ricoeur": "Filósofo francés que integró hermenéutica, fenomenología y estructuralismo. Sus trabajos sobre narratividad, memoria e identidad personal son fundamentales. Desarrolló una 'hermenéutica del sí mismo' y contribuyó significativamente a la filosofía del lenguaje y la ética.",
        
        "Walter Benjamin": "Filósofo y crítico cultural alemán asociado con la Escuela de Frankfurt. Sus ensayos sobre arte, literatura y cultura moderna, como 'La obra de arte en la época de su reproductibilidad técnica', fueron revolucionarios. Su pensamiento combina marxismo, misticismo judío y crítica estética.",
        
        "Antonio Gramsci": "Filósofo y teórico político italiano, fundador del Partido Comunista Italiano. Desarrolló conceptos como 'hegemonía cultural' y 'intelectual orgánico'. Sus 'Cuadernos de la cárcel', escritos durante su encarcelamiento fascista, renovaron profundamente la teoría marxista.",
        
        "Michel Foucault": "Filósofo francés del siglo XX, figura clave del postestructuralismo. Sus análisis sobre poder, saber y sexualidad revolucionaron las ciencias humanas. Obras como 'Historia de la locura', 'Vigilar y castigar' y 'Historia de la sexualidad' influyeron profundamente en filosofía, sociología e historia."
    }
    
    # Si existe biografía detallada, devolverla
    if name in DETAILED_BIOGRAPHIES:
        return DETAILED_BIOGRAPHIES[name]
    
    # Biografías más específicas por categoría para otros filósofos
    generic_biographies = {
        # Presocráticos
        "Tales de Mileto": f"{name}, considerado el primer filósofo occidental, propuso que el agua es el principio fundamental de todas las cosas. Fue también matemático y astrónomo, miembro de los Siete Sabios de Grecia.",
        "Anaximandro": f"{name}, discípulo de Tales, propuso el 'ápeiron' (lo indefinido) como principio universal. Creó el primer mapa del mundo conocido y desarrolló teorías evolutivas primitivas.",
        "Anaxímenes": f"{name}, último filósofo de Mileto, consideró el aire como elemento primordial. Sus teorías sobre condensación y rarefacción influyeron en cosmogonías posteriores.",
        
        # Neoplatónicos
        "Plotino": f"{name}, fundador del neoplatonismo, desarrolló la filosofía de las tres hipóstasis: el Uno, el Intelecto y el Alma. Sus 'Enéadas' influyeron profundamente en el cristianismo.",
        "Proclo": f"{name} fue el último gran filósofo neoplatónico que dirigió la Academia platónica. Desarrolló una compleja teología filosófica que influyó en el pensamiento medieval.",
        
        # Filósofos Medievales menores
        "Anselmo de Canterbury": f"{name}, arzobispo y filósofo del siglo XI, famoso por su argumento ontológico para demostrar la existencia de Dios y el principio 'fides quaerens intellectum'.",
        "Pedro Abelardo": f"{name}, filósofo escolástico del siglo XII, desarrolló la dialéctica teológica. Su historia amorosa con Eloísa y su conceptualismo lo convirtieron en figura emblemática.",
        
        # Filósofos Orientales
        "Nagarjuna": f"{name}, filósofo budista del siglo II, fundó la escuela Madhyamaka. Desarrolló la doctrina de la vacuidad (sunyata) y el camino medio budista.",
        "Mencio": f"{name}, filósofo confuciano chino, desarrolló la teoría de la bondad intrínseca de la naturaleza humana y defendió el gobierno benevolente.",
        "Zhuangzi": f"{name}, filósofo taoísta chino, escribió textos llenos de paradojas sobre la relatividad, transformación constante y libertad espiritual."
    }
    
    if name in generic_biographies:
        return generic_biographies[name]
    
    # Fallback genérico pero más informativo
    return f"{name} fue un filósofo influyente cuyo pensamiento contribuyó significativamente al desarrollo de la tradición filosófica occidental y oriental."