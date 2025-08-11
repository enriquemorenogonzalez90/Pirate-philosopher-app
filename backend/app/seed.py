from datetime import date
import random
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select
from urllib.parse import quote_plus
import requests

from .models import Author, School, Book, Quote, author_school_table


AUTHOR_NAMES = [
    "Sócrates", "Platón", "Aristóteles", "Epicuro", "Zenón de Citio",
    "Pitágoras", "Heráclito", "Parménides", "Diógenes", "Séneca",
    "Marco Aurelio", "Tomás de Aquino", "San Agustín", "René Descartes", "Baruch Spinoza",
    "John Locke", "David Hume", "Immanuel Kant", "Georg Hegel", "Friedrich Nietzsche",
    "Søren Kierkegaard", "Karl Marx", "Arthur Schopenhauer", "Ludwig Wittgenstein", "Bertrand Russell",
    "Martin Heidegger", "Jean-Paul Sartre", "Simone de Beauvoir", "Hannah Arendt", "Michel Foucault",
    "Gilles Deleuze", "Jacques Derrida", "Jürgen Habermas", "Paul Ricoeur", "Karl Popper",
    "Thomas Kuhn", "John Rawls", "Noam Chomsky", "Martha Nussbaum", "Judith Butler"
]

SCHOOL_DATA = [
    {"nombre": "Estoicismo", "descripcion": "Escuela filosófica helenística fundada en Atenas por Zenón de Citio. Enseña que la virtud, única fuente del bien, se basa en el conocimiento y que los sabios viven en armonía con la razón divina que gobierna la naturaleza."},
    {"nombre": "Epicureísmo", "descripcion": "Escuela filosófica fundada por Epicuro en Atenas. Propone que el placer es el bien supremo y el objetivo de la vida humana, pero entendido como ausencia de dolor (ataraxia) y no como hedonismo vulgar."},
    {"nombre": "Cínicos", "descripcion": "Escuela filosófica griega fundada por Antístenes. Defienden una vida ascética en armonía con la naturaleza, despreciando las convenciones sociales y buscando la autosuficiencia (autarquía)."},
    {"nombre": "Escépticos", "descripcion": "Corriente filosófica que cuestiona la posibilidad del conocimiento cierto. Propone la suspensión del juicio (epoché) como medio para alcanzar la tranquilidad del alma (ataraxia)."},
    {"nombre": "Platonismo", "descripcion": "Tradición filosófica basada en las enseñanzas de Platón. Defiende la existencia de un mundo de Ideas o Formas perfectas e inmutables, del cual el mundo sensible es una mera copia imperfecta."},
    {"nombre": "Aristotelismo", "descripcion": "Sistema filosófico desarrollado por Aristóteles. Enfatiza la observación empírica, la lógica formal y la búsqueda de las causas naturales de los fenómenos, rechazando el mundo de las Ideas platónico."},
    {"nombre": "Neoplatonismo", "descripcion": "Corriente filosófica que reinterpreta el platonismo incorporando elementos místicos. Desarrollada por Plotino, propone una jerarquía de la realidad que emana del Uno absoluto."},
    {"nombre": "Escolástica", "descripcion": "Método filosófico y teológico medieval que busca reconciliar la fe cristiana con la razón aristotélica. Desarrollada en las universidades medievales, alcanza su máxima expresión con Tomás de Aquino."},
    {"nombre": "Racionalismo", "descripcion": "Corriente filosófica moderna que sostiene que la razón es la fuente principal del conocimiento. Representada por Descartes, Spinoza y Leibniz, confía en el poder de la mente para conocer la realidad."},
    {"nombre": "Empirismo", "descripcion": "Escuela filosófica que afirma que todo conocimiento deriva de la experiencia sensorial. Desarrollada por filósofos británicos como Locke, Berkeley y Hume, se opone al racionalismo continental."},
    {"nombre": "Idealismo alemán", "descripcion": "Movimiento filosófico alemán que sostiene que la realidad es fundamentalmente mental o espiritual. Iniciado por Kant y desarrollado por Fichte, Schelling y Hegel."},
    {"nombre": "Existencialismo", "descripcion": "Corriente filosófica que enfatiza la existencia individual, la libertad de elección y la responsabilidad personal. Desarrollada por Kierkegaard, Nietzsche, Heidegger y Sartre."},
    {"nombre": "Fenomenología", "descripcion": "Método filosófico que estudia las estructuras de la experiencia tal como se presentan a la conciencia, sin recurrir a teorías sobre su existencia real. Fundada por Edmund Husserl."},
    {"nombre": "Estructuralismo", "descripcion": "Corriente que analiza los fenómenos culturales como sistemas de signos, enfocándose en las relaciones estructurales subyacentes más que en los elementos individuales."},
    {"nombre": "Posmodernismo", "descripcion": "Movimiento intelectual que critica las narrativas universales de la modernidad, cuestionando conceptos como verdad absoluta, progreso y razón universal."},
    {"nombre": "Utilitarismo", "descripcion": "Teoría ética que juzga las acciones por sus consecuencias, buscando maximizar la felicidad o bienestar general. Desarrollada por Jeremy Bentham y John Stuart Mill."},
    {"nombre": "Pragmatismo", "descripcion": "Escuela filosófica americana que evalúa las ideas por su utilidad práctica y sus consecuencias. Fundada por Charles Sanders Peirce y desarrollada por William James y John Dewey."},
    {"nombre": "Analítica", "descripcion": "Tradición filosófica que enfatiza la claridad, el rigor lógico y el análisis del lenguaje como herramientas para resolver problemas filosóficos. Dominante en el mundo anglosajón."},
    {"nombre": "Hermenéutica", "descripcion": "Filosofía de la interpretación que estudia cómo comprendemos textos, acciones y expresiones humanas. Desarrollada por Dilthey, Heidegger y Gadamer."},
    {"nombre": "Crítica", "descripcion": "Corriente que busca desenmascarar las estructuras de poder ocultas en la sociedad y el conocimiento, promoviendo la emancipación social. Asociada con la Escuela de Frankfurt."}
]

AUTHOR_DATA = {
    "Sócrates": {
        "libros": ["Apología de Sócrates (Platón)", "Critón (Platón)", "Fedón (Platón)"],
        "fecha_nacimiento": date(470, 1, 1),
        "fecha_defuncion": date(399, 1, 1),
        "biografia": "Sócrates (470-399 a.C.) fue un filósofo griego considerado uno de los fundadores de la filosofía occidental. Nacido en Atenas, desarrolló el método socrático de investigación filosófica mediante preguntas. No escribió ninguna obra, y conocemos su pensamiento a través de los diálogos de su discípulo Platón. Su filosofía se centró en la ética y el conocimiento de sí mismo, famoso por la frase 'solo sé que no sé nada'. Fue condenado a muerte por corromper a la juventud y no reconocer a los dioses de la ciudad, muriendo al beber cicuta. Su influencia en el pensamiento occidental es inmensa, siendo considerado el padre del pensamiento racional y la ética."
    },
    "Platón": {
        "libros": ["La República", "Fedro", "Banquete", "Menón", "Timeo"],
        "fecha_nacimiento": date(428, 1, 1),
        "fecha_defuncion": date(348, 1, 1),
        "biografia": "Platón (428-348 a.C.) fue un filósofo griego, discípulo de Sócrates y maestro de Aristóteles. Fundó la Academia de Atenas, considerada la primera institución de educación superior de Occidente. Su filosofía se basa en la teoría de las Ideas o Formas, según la cual existe un mundo perfecto e inmutable de conceptos puros, del cual nuestro mundo material es solo una copia imperfecta. En política, propuso en 'La República' un estado ideal gobernado por filósofos-reyes. Sus diálogos, protagonizados generalmente por Sócrates, abordan temas como la justicia, la verdad, la belleza y el amor. Su influencia en la filosofía, la ciencia y la educación occidental ha sido fundamental durante más de dos milenios."
    },
    "Aristóteles": {
        "libros": ["Ética a Nicómaco", "Política", "Metafísica", "Poética", "Física"],
        "fecha_nacimiento": date(384, 1, 1),
        "fecha_defuncion": date(322, 1, 1),
        "biografia": "Aristóteles (384-322 a.C.) fue un filósofo griego, discípulo de Platón y tutor de Alejandro Magno. Fundó el Liceo en Atenas y desarrolló un sistema filosófico que abarcó prácticamente todas las áreas del conocimiento humano. A diferencia de su maestro Platón, Aristóteles enfatizó la observación empírica y la experiencia sensorial como fuentes de conocimiento. Desarrolló la lógica formal, clasificó las ciencias, estudió la biología, la física, la ética y la política. Su concepto de la 'causa final' y su teoría del 'justo medio' en ética han sido fundamentales. Su influencia se extiende desde la filosofía medieval hasta la ciencia moderna, siendo conocido como 'El Filósofo' durante la Edad Media."
    },
    "Epicuro": {
        "libros": ["Carta a Meneceo", "Máximas Capitales", "Carta a Heródoto"],
        "fecha_nacimiento": date(341, 1, 1),
        "fecha_defuncion": date(270, 1, 1),
        "biografia": "Epicuro (341-270 a.C.) fue un filósofo griego fundador del epicureísmo. Estableció el Jardín en Atenas, una comunidad filosófica que admitía mujeres y esclavos. Su filosofía se centró en la búsqueda de la felicidad a través del placer, pero entendido como ausencia de dolor (ataraxia) y perturbación (apatía). Desarrolló una ética hedonista racional que enfatizaba los placeres simples y duraderos sobre los momentáneos. Su física atomista, influenciada por Demócrito, explicaba el universo como resultado del movimiento azaroso de átomos en el vacío, negando la intervención divina en los asuntos humanos."
    },
    "René Descartes": {
        "libros": ["Discurso del Método", "Meditaciones Metafísicas", "Principios de Filosofía"],
        "fecha_nacimiento": date(1596, 3, 31),
        "fecha_defuncion": date(1650, 2, 11),
        "biografia": "René Descartes (1596-1650) fue un filósofo, matemático y científico francés, considerado el padre de la filosofía moderna. Desarrolló el método cartesiano de duda metódica, partiendo del famoso 'cogito ergo sum' (pienso, luego existo) como primera certeza indudable. Su dualismo mente-cuerpo influyó profundamente en la filosofía occidental. Contribuyó significativamente a las matemáticas con la geometría analítica y el sistema de coordenadas cartesianas. Su racionalismo enfatizaba la razón como fuente principal del conocimiento, estableciendo las bases del pensamiento científico moderno."
    },
    "Immanuel Kant": {
        "libros": ["Crítica de la Razón Pura", "Crítica de la Razón Práctica", "Crítica del Juicio"],
        "fecha_nacimiento": date(1724, 4, 22),
        "fecha_defuncion": date(1804, 2, 12),
        "biografia": "Immanuel Kant (1724-1804) fue un filósofo alemán de la Ilustración, considerado uno de los pensadores más influyentes de la historia. Desarrolló la filosofía crítica o trascendental, intentando superar el conflicto entre racionalismo y empirismo. Su 'Crítica de la Razón Pura' examina los límites del conocimiento humano, introduciendo conceptos como los juicios sintéticos a priori y las categorías del entendimiento. En ética, formuló el imperativo categórico como principio moral universal. Su filosofía política defendió la paz perpetua y el republicanismo. Revolucionó campos como la epistemología, la ética, la estética y la filosofía política."
    },
    "Friedrich Nietzsche": {
        "libros": ["Así Habló Zaratustra", "Más Allá del Bien y del Mal", "La Genealogía de la Moral"],
        "fecha_nacimiento": date(1844, 10, 15),
        "fecha_defuncion": date(1900, 8, 25),
        "biografia": "Friedrich Nietzsche (1844-1900) fue un filósofo alemán cuyo pensamiento influyó profundamente en la filosofía contemporánea. Proclamó la 'muerte de Dios' y criticó duramente la moral cristiana y los valores tradicionales occidentales. Desarrolló conceptos como el 'superhombre' (Übermensch), la 'voluntad de poder' y el 'eterno retorno'. Su genealogía de la moral analizó los orígenes psicológicos y históricos de los valores morales. Aunque su obra fue malinterpretada y utilizada por regímenes totalitarios, su crítica de la modernidad y su llamada a la revaluación de todos los valores han sido fundamentales para el pensamiento postmoderno."
    },
    "Jean-Paul Sartre": {
        "libros": ["El Ser y la Nada", "La Náusea", "El Existencialismo es un Humanismo"],
        "fecha_nacimiento": date(1905, 6, 21),
        "fecha_defuncion": date(1980, 4, 15),
        "biografia": "Jean-Paul Sartre (1905-1980) fue un filósofo, escritor y crítico francés, figura central del existencialismo. Desarrolló la idea de que 'la existencia precede a la esencia', argumentando que los humanos primero existen y luego crean su propia esencia a través de sus decisiones libres. Su filosofía enfatiza la libertad radical, la responsabilidad absoluta y la 'angustia' existencial. Además de su trabajo filosófico, fue un prolífico escritor de novelas, obras de teatro y ensayos políticos. Comprometido políticamente, apoyó movimientos de izquierda y fue un intelectual público influyente. Rechazó el Premio Nobel de Literatura en 1964."
    },
    "Zenón de Citio": {
        "libros": ["Sobre la República", "Sobre los Signos", "Sobre la Naturaleza"],
        "fecha_nacimiento": date(334, 1, 1),
        "fecha_defuncion": date(262, 1, 1),
        "biografia": "Zenón de Citio (334-262 a.C.) fue un filósofo griego fundador del estoicismo. Estableció su escuela en la Stoa Poikile (Pórtico Pintado) de Atenas, de donde deriva el nombre 'estoicismo'. Su filosofía enfatizaba la virtud como el único bien verdadero y la importancia de vivir conforme a la naturaleza y la razón."
    },
    "Pitágoras": {
        "libros": ["Versos Dorados", "Sobre la Naturaleza", "Sobre los Números"],
        "fecha_nacimiento": date(570, 1, 1),
        "fecha_defuncion": date(495, 1, 1),
        "biografia": "Pitágoras (570-495 a.C.) fue un filósofo y matemático griego. Fundó una escuela filosófica y religiosa que influyó significativamente en Platón. Es conocido por el teorema de Pitágoras en matemáticas y por sus ideas sobre la transmigración de las almas y la armonía de las esferas."
    },
    "Heráclito": {
        "libros": ["Sobre la Naturaleza", "Fragmentos", "Sobre el Logos"],
        "fecha_nacimiento": date(535, 1, 1),
        "fecha_defuncion": date(475, 1, 1),
        "biografia": "Heráclito de Éfeso (535-475 a.C.) fue un filósofo presocrático conocido por su doctrina del flujo perpetuo y la unidad de los opuestos. Famoso por la frase 'nadie se baña en el mismo río dos veces', enfatizó el cambio constante como la característica fundamental de la realidad."
    },
    "Parménides": {
        "libros": ["Sobre la Naturaleza", "El Poema", "Sobre el Ser"],
        "fecha_nacimiento": date(515, 1, 1),
        "fecha_defuncion": date(450, 1, 1),
        "biografia": "Parménides de Elea (515-450 a.C.) fue un filósofo presocrático fundador de la escuela eleática. Su poema filosófico 'Sobre la Naturaleza' distingue entre el 'camino de la verdad' y el 'camino de la opinión', argumentando que el cambio es ilusorio y que la realidad es una, eterna e inmutable."
    },
    "Diógenes": {
        "libros": ["Cartas", "Tragedias", "Sobre la Virtud"],
        "fecha_nacimiento": date(412, 1, 1),
        "fecha_defuncion": date(323, 1, 1),
        "biografia": "Diógenes de Sínope (412-323 a.C.) fue un filósofo griego y figura central del cinismo. Conocido por su estilo de vida ascético y sus provocaciones públicas, vivía en extrema pobreza y criticaba las convenciones sociales. Sus enseñanzas enfatizaban la autosuficiencia y el desprecio por las posesiones materiales."
    },
    "Séneca": {
        "libros": ["Cartas a Lucilio", "Sobre la Clemencia", "Sobre la Ira", "Meditaciones"],
        "fecha_nacimiento": date(4, 1, 1),
        "fecha_defuncion": date(65, 1, 1),
        "biografia": "Lucio Anneo Séneca (4-65 d.C.) fue un filósofo estoico, político y dramaturgo romano. Fue tutor y consejero del emperador Nerón. Sus obras sobre filosofía estoica, especialmente sus cartas morales, han sido influyentes durante siglos, enfatizando la importancia de la virtud, la razón y la aceptación del destino."
    },
    "Marco Aurelio": {
        "libros": ["Meditaciones", "Pensamientos", "Reflexiones"],
        "fecha_nacimiento": date(121, 4, 26),
        "fecha_defuncion": date(180, 3, 17),
        "biografia": "Marco Aurelio (121-180 d.C.) fue emperador romano y filósofo estoico. Sus 'Meditaciones', escritas como reflexiones personales, representan una de las obras más importantes del estoicismo tardío. Combinó el poder político con la sabiduría filosófica, siendo considerado uno de los 'cinco buenos emperadores'."
    },
    "Tomás de Aquino": {
        "libros": ["Suma Teológica", "Suma contra Gentiles", "Sobre el Ente y la Esencia"],
        "fecha_nacimiento": date(1225, 1, 28),
        "fecha_defuncion": date(1274, 3, 7),
        "biografia": "Santo Tomás de Aquino (1225-1274) fue un teólogo y filósofo escolástico italiano. Integró la filosofía aristotélica con la doctrina cristiana, desarrollando una síntesis que influyó profundamente en la teología católica. Su 'Suma Teológica' es considerada una obra maestra de la filosofía medieval."
    },
    "San Agustín": {
        "libros": ["Confesiones", "La Ciudad de Dios", "Sobre la Trinidad"],
        "fecha_nacimiento": date(354, 11, 13),
        "fecha_defuncion": date(430, 8, 28),
        "biografia": "San Agustín de Hipona (354-430) fue un teólogo y filósofo cristiano. Sus 'Confesiones' son consideradas la primera autobiografía occidental. Influyó enormemente en el desarrollo de la filosofía y teología cristianas, integrando elementos platónicos con la doctrina cristiana."
    },
    "Baruch Spinoza": {
        "libros": ["Ética", "Tratado Teológico-Político", "Tratado de la Reforma del Entendimiento"],
        "fecha_nacimiento": date(1632, 11, 24),
        "fecha_defuncion": date(1677, 2, 21),
        "biografia": "Baruch Spinoza (1632-1677) fue un filósofo racionalista holandés de origen judío. Desarrolló un sistema filosófico monista que identificaba a Dios con la naturaleza. Su 'Ética' presenta una visión determinista del universo y una filosofía que busca la felicidad a través del conocimiento racional."
    },
    "John Locke": {
        "libros": ["Ensayo sobre el Entendimiento Humano", "Dos Tratados sobre el Gobierno Civil"],
        "fecha_nacimiento": date(1632, 8, 29),
        "fecha_defuncion": date(1704, 10, 28),
        "biografia": "John Locke (1632-1704) fue un filósofo empirista inglés. Desarrolló la teoría de la mente como 'tabula rasa' y fue fundamental en el desarrollo del liberalismo político. Sus ideas sobre el gobierno y los derechos naturales influyeron en las revoluciones americana y francesa."
    },
    "David Hume": {
        "libros": ["Tratado de la Naturaleza Humana", "Investigación sobre el Entendimiento Humano"],
        "fecha_nacimiento": date(1711, 5, 7),
        "fecha_defuncion": date(1776, 8, 25),
        "biografia": "David Hume (1711-1776) fue un filósofo, economista e historiador escocés. Desarrolló un empirismo escéptico que cuestionó la causalidad y la inducción. Su crítica de la razón influyó profundamente en Kant y en el desarrollo de la filosofía moderna."
    },
    "Georg Hegel": {
        "libros": ["Fenomenología del Espíritu", "Ciencia de la Lógica", "Filosofía del Derecho"],
        "fecha_nacimiento": date(1770, 8, 27),
        "fecha_defuncion": date(1831, 11, 14),
        "biografia": "Georg Wilhelm Friedrich Hegel (1770-1831) fue un filósofo alemán del idealismo. Desarrolló un sistema dialéctico que explica el desarrollo de la realidad a través de contradicciones y síntesis. Su influencia se extiende desde la filosofía política hasta la filosofía de la historia."
    },
    "Søren Kierkegaard": {
        "libros": ["Temor y Temblor", "El Concepto de la Angustia", "Diario de un Seductor"],
        "fecha_nacimiento": date(1813, 5, 5),
        "fecha_defuncion": date(1855, 11, 11),
        "biografia": "Søren Kierkegaard (1813-1855) fue un teólogo y filósofo danés, considerado precursor del existencialismo. Enfatizó la importancia de la elección individual y la experiencia subjetiva. Su análisis de la angustia, la fe y la desesperación influyó profundamente en la filosofía existencial."
    },
    "Karl Marx": {
        "libros": ["El Capital", "Manifiesto Comunista", "Manuscritos Económico-Filosóficos"],
        "fecha_nacimiento": date(1818, 5, 5),
        "fecha_defuncion": date(1883, 3, 14),
        "biografia": "Karl Marx (1818-1883) fue un filósofo, economista y revolucionario alemán. Desarrolló una crítica del capitalismo y una teoría de la historia basada en la lucha de clases. Sus ideas sobre el materialismo histórico y la economía política han influido enormemente en la política y la sociología modernas."
    },
    "Arthur Schopenhauer": {
        "libros": ["El Mundo como Voluntad y Representación", "Sobre el Fundamento de la Moral"],
        "fecha_nacimiento": date(1788, 2, 22),
        "fecha_defuncion": date(1860, 9, 21),
        "biografia": "Arthur Schopenhauer (1788-1860) fue un filósofo alemán conocido por su pesimismo filosófico. Desarrolló una metafísica de la voluntad, argumentando que el sufrimiento es inherente a la existencia. Su filosofía influyó en Nietzsche, Wagner y muchos escritores y artistas posteriores."
    },
    "Ludwig Wittgenstein": {
        "libros": ["Tractatus Logico-Philosophicus", "Investigaciones Filosóficas"],
        "fecha_nacimiento": date(1889, 4, 26),
        "fecha_defuncion": date(1951, 4, 29),
        "biografia": "Ludwig Wittgenstein (1889-1951) fue un filósofo austriaco-británico. Realizó contribuciones fundamentales a la lógica, la filosofía del lenguaje y la filosofía de la mente. Su obra se divide en dos períodos: el primer Wittgenstein del 'Tractus' y el segundo de las 'Investigaciones Filosóficas'."
    },
    "Bertrand Russell": {
        "libros": ["Principia Mathematica", "Los Problemas de la Filosofía", "Historia de la Filosofía Occidental"],
        "fecha_nacimiento": date(1872, 5, 18),
        "fecha_defuncion": date(1970, 2, 2),
        "biografia": "Bertrand Russell (1872-1970) fue un filósofo, lógico y matemático británico. Contribuyó significativamente al desarrollo de la lógica matemática y la filosofía analítica. También fue un prominente activista político y social, ganador del Premio Nobel de Literatura en 1950."
    },
    "Martin Heidegger": {
        "libros": ["Ser y Tiempo", "La Pregunta por la Técnica", "Carta sobre el Humanismo"],
        "fecha_nacimiento": date(1889, 9, 26),
        "fecha_defuncion": date(1976, 5, 26),
        "biografia": "Martin Heidegger (1889-1976) fue un filósofo alemán cuya obra se centra en la pregunta por el ser. Su análisis existencial del Dasein (ser-ahí) en 'Ser y Tiempo' influyó profundamente en la fenomenología, el existencialismo y la hermenéutica contemporánea."
    },
    "Simone de Beauvoir": {
        "libros": ["El Segundo Sexo", "La Ética de la Ambigüedad", "Los Mandarines"],
        "fecha_nacimiento": date(1908, 1, 9),
        "fecha_defuncion": date(1986, 4, 14),
        "biografia": "Simone de Beauvoir (1908-1986) fue una escritora, filósofa y feminista francesa. Su obra 'El Segundo Sexo' es fundamental para el feminismo moderno. Compañera intelectual de Sartre, desarrolló ideas existencialistas y análisis pioneros sobre la condición de la mujer."
    },
    "Hannah Arendt": {
        "libros": ["Los Orígenes del Totalitarismo", "La Condición Humana", "Eichmann en Jerusalén"],
        "fecha_nacimiento": date(1906, 10, 14),
        "fecha_defuncion": date(1975, 12, 4),
        "biografia": "Hannah Arendt (1906-1975) fue una filósofa política alemana-estadounidense. Sus análisis del totalitarismo, la autoridad y la naturaleza del poder han sido fundamentales para la teoría política contemporánea. Su concepto de 'banalidad del mal' revolucionó la comprensión de los crímenes políticos."
    },
    "Michel Foucault": {
        "libros": ["Vigilar y Castigar", "Historia de la Sexualidad", "Las Palabras y las Cosas"],
        "fecha_nacimiento": date(1926, 10, 15),
        "fecha_defuncion": date(1984, 6, 25),
        "biografia": "Michel Foucault (1926-1984) fue un filósofo e historiador francés. Sus análisis de las instituciones sociales, especialmente la psiquiatría, la medicina, las ciencias humanas y el sistema penitenciario, han influido enormemente en la sociología, la antropología y los estudios culturales."
    }
}


QUOTES = [
    "Conócete a ti mismo.",
    "El hombre es la medida de todas las cosas.",
    "Solo sé que no sé nada.",
    "La felicidad depende de nosotros mismos.",
    "El carácter es el destino.",
    "Vive de acuerdo con la naturaleza.",
    "El placer es el principio y fin de la vida feliz.",
    "La libertad es la obediencia a la ley que uno mismo se da.",
    "Dios ha muerto.",
    "El tiempo es una imagen móvil de la eternidad.",
    "La vida examinada no vale la pena ser vivida.",
    "El conocimiento es poder.",
    "Pienso, luego existo.",
    "No hay nada en el entendimiento que no haya estado antes en los sentidos.",
    "La razón pura es la fuente de la moral.",
    "El ser y la nada.",
    "La historia es la marcha de la libertad.",
    "La verdad es hija del tiempo.",
    "El hombre nace libre, pero en todos lados está encadenado.",
    "La filosofía es la preparación para la muerte.",
    "La existencia precede a la esencia.",
    "La opresión produce la violencia.",
    "La verdad es relativa a los juegos de lenguaje.",
    "El poder produce saber.",
    "No hay hechos, solo interpretaciones.",
    "La empatía es fundamento de la justicia.",
    "La democracia es un experimento.",
    "La imaginación moral es central para la vida buena.",
    "La justicia como equidad.",
    "La refutabilidad es el criterio de la ciencia.",
    "Los paradigmas guían la ciencia.",
    "La acción comunicativa busca el entendimiento.",
    "El cuidado de sí.",
    "La dialéctica del amo y el esclavo.",
    "La virtud es conocimiento.",
    "El logos gobierna el cosmos.",
    "La virtud es suficiente para la felicidad.",
    "El hombre es un animal político.",
    "El lenguaje es un juego.",
    "La vida del espíritu es la vida del mundo."
]


def fetch_wikipedia_portrait(nombre: str) -> Optional[str]:
    """Busca miniatura en Wikipedia (es y fallback en). Devuelve URL o None."""
    titles = [nombre, nombre.replace("á", "a").replace("é", "e").replace("í", "i").replace("ó", "o").replace("ú", "u")]
    langs = ["es", "en"]
    for lang in langs:
        for title in titles:
            try:
                resp = requests.get(
                    f"https://{lang}.wikipedia.org/w/api.php",
                    params={
                        "action": "query",
                        "format": "json",
                        "prop": "pageimages|pageterms",
                        "piprop": "thumbnail",
                        "pithumbsize": 512,
                        "titles": title,
                        "redirects": 1,
                    },
                    timeout=6,
                )
                if resp.status_code != 200:
                    continue
                data = resp.json()
                pages = data.get("query", {}).get("pages", {})
                for page in pages.values():
                    thumb = page.get("thumbnail", {})
                    src = thumb.get("source")
                    if src:
                        return src
            except Exception:
                continue
    return None


def fetch_wikipedia_school_image(nombre: str) -> Optional[str]:
    """Busca imagen de escuela en Wikipedia (es y fallback en). Devuelve URL o None."""
    # Mapeo de nombres de escuelas a términos de búsqueda más específicos
    search_terms = {
        "Estoicismo": ["Estoicismo", "Stoicism", "Escuela estoica"],
        "Epicureísmo": ["Epicureísmo", "Epicureanism", "Jardín de Epicuro"],
        "Cínicos": ["Cínicos", "Cynicism", "Escuela cínica"],
        "Escépticos": ["Escepticismo", "Skepticism", "Escuela escéptica"],
        "Platonismo": ["Platonismo", "Platonism", "Academia de Platón"],
        "Aristotelismo": ["Aristotelismo", "Aristotelianism", "Liceo"],
        "Neoplatonismo": ["Neoplatonismo", "Neoplatonism", "Plotino"],
        "Escolástica": ["Escolástica", "Scholasticism", "Escuela escolástica"],
        "Racionalismo": ["Racionalismo", "Rationalism", "Descartes"],
        "Empirismo": ["Empirismo", "Empiricism", "John Locke"],
        "Idealismo alemán": ["Idealismo alemán", "German idealism", "Hegel"],
        "Existencialismo": ["Existencialismo", "Existentialism", "Sartre"],
        "Fenomenología": ["Fenomenología", "Phenomenology", "Husserl"],
        "Estructuralismo": ["Estructuralismo", "Structuralism", "Levi-Strauss"],
        "Posmodernismo": ["Posmodernismo", "Postmodernism", "Derrida"],
        "Utilitarismo": ["Utilitarismo", "Utilitarianism", "Jeremy Bentham"],
        "Pragmatismo": ["Pragmatismo", "Pragmatism", "William James"],
        "Analítica": ["Filosofía analítica", "Analytic philosophy", "Russell"],
        "Hermenéutica": ["Hermenéutica", "Hermeneutics", "Gadamer"],
        "Crítica": ["Teoría crítica", "Critical theory", "Frankfurt School"],
        "Marxismo": ["Marxismo", "Marxism", "Karl Marx"],
        "Positivismo": ["Positivismo", "Positivism", "Auguste Comte"],
        "Constructivismo": ["Constructivismo", "Constructivism", "Piaget"],
        "Feminismo": ["Feminismo", "Feminism", "Simone de Beauvoir"],
        "Liberalismo": ["Liberalismo", "Liberalism", "John Stuart Mill"],
        "Realismo": ["Realismo filosófico", "Philosophical realism", "Aristotle"],
        "Naturalismo": ["Naturalismo", "Naturalism", "John Dewey"],
        "Humanismo": ["Humanismo", "Humanism", "Erasmo"],
        "Vitalismo": ["Vitalismo", "Vitalism", "Henri Bergson"],
        "Nihilismo": ["Nihilismo", "Nihilism", "Nietzsche"],
        "Deconstrucción": ["Deconstrucción", "Deconstruction", "Derrida"],
        "Dialéctica": ["Dialéctica", "Dialectic", "Hegel"],
        "Estoicismo Romano": ["Estoicismo romano", "Roman Stoicism", "Seneca"],
        "Ilustración": ["Ilustración", "Age of Enlightenment", "Voltaire"],
        "Romanticismo": ["Romanticismo", "Romanticism", "Rousseau"],
        "Ilustración Escocesa": ["Ilustración escocesa", "Scottish Enlightenment", "Hume"],
        "Teoría Crítica": ["Teoría crítica", "Critical theory", "Adorno"],
        "Poscolonialismo": ["Poscolonialismo", "Postcolonialism", "Said"],
        "Neoescolástica": ["Neoescolástica", "Neo-Scholasticism", "Maritain"],
        "Eudemonismo": ["Eudemonismo", "Eudaimonism", "Aristotle"]
    }
    
    search_list = search_terms.get(nombre, [nombre])
    langs = ["es", "en"]
    
    for lang in langs:
        for term in search_list:
            try:
                resp = requests.get(
                    f"https://{lang}.wikipedia.org/w/api.php",
                    params={
                        "action": "query",
                        "format": "json",
                        "prop": "pageimages|pageterms",
                        "piprop": "thumbnail",
                        "pithumbsize": 512,
                        "titles": term,
                        "redirects": 1,
                    },
                    timeout=6,
                )
                if resp.status_code != 200:
                    continue
                data = resp.json()
                pages = data.get("query", {}).get("pages", {})
                for page in pages.values():
                    thumb = page.get("thumbnail", {})
                    src = thumb.get("source")
                    if src:
                        return src
            except Exception:
                continue
    return None


def author_image_url(name: str) -> str:
    # fallback local a avatar si no hay retrato
    encoded = quote_plus(name)
    return f"https://ui-avatars.com/api/?name={encoded}&background=0D8ABC&color=fff&size=256&bold=true"


def school_image_url(name: str) -> str:
    # fallback local a avatar si no hay imagen
    encoded = quote_plus(name)
    return f"https://ui-avatars.com/api/?name={encoded}&background=8B4513&color=fff&size=256&bold=true"


def fetch_book_cover(titulo: str, autor: str) -> Optional[str]:
    """Busca la portada de un libro en Open Library API"""
    try:
        # Buscar por título y autor
        search_query = f"{titulo} {autor}".replace(" ", "+")
        search_url = f"https://openlibrary.org/search.json?q={search_query}&limit=1"
        
        resp = requests.get(search_url, timeout=5)
        if resp.status_code != 200:
            return None
            
        data = resp.json()
        docs = data.get("docs", [])
        
        if docs and "cover_i" in docs[0]:
            cover_id = docs[0]["cover_i"]
            # Obtener la imagen de portada
            cover_url = f"https://covers.openlibrary.org/b/id/{cover_id}-L.jpg"
            return cover_url
            
    except Exception:
        pass
    
    return None


def book_placeholder_url(titulo: str) -> str:
    """URL de imagen placeholder para libros"""
    # Crear una imagen simple con el título del libro
    encoded_title = quote_plus(titulo[:30])  # Limitar a 30 caracteres
    return f"https://ui-avatars.com/api/?name={encoded_title}&background=2563eb&color=fff&size=200&bold=true&format=png"


def seed_data_if_needed(session: Session) -> None:
    existing = session.execute(select(Author)).scalars().first()
    if existing:
        return

    authors: List[Author] = []
    schools: List[School] = []

    for i in range(40):
        name = AUTHOR_NAMES[i % len(AUTHOR_NAMES)]
        portrait = fetch_wikipedia_portrait(name) or author_image_url(name)
        
        # Obtener datos específicos del autor si están disponibles
        author_info = AUTHOR_DATA.get(name, {})
        if isinstance(author_info, dict):
            fecha_nac = author_info.get("fecha_nacimiento")
            fecha_def = author_info.get("fecha_defuncion")
            biografia = author_info.get("biografia", f"Biografía detallada de {name}.")
        else:
            # Datos por defecto para autores sin información específica
            fecha_nac = None
            fecha_def = None
            biografia = f"Biografía detallada de {name}."
        
        author = Author(
            nombre=name,
            epoca=random.choice(["Antigua", "Medieval", "Moderna", "Contemporánea"]),
            fecha_nacimiento=fecha_nac,
            fecha_defuncion=fecha_def,
            imagen_url=portrait,
            biografia=biografia
        )
        session.add(author)
        authors.append(author)

    for i in range(len(SCHOOL_DATA)):
        school_data = SCHOOL_DATA[i]
        name = school_data["nombre"]
        image = fetch_wikipedia_school_image(name) or school_image_url(name)
        school = School(
            nombre=name,
            imagen_url=image,
            descripcion=school_data["descripcion"]
        )
        session.add(school)
        schools.append(school)

    session.commit()
    session.refresh(authors[0])
    session.refresh(schools[0])

    # Vincular autores con 1-3 escuelas
    for author in authors:
        linked = random.sample(schools, k=random.randint(1, 3))
        for sc in linked:
            session.execute(author_school_table.insert().values(author_id=author.id, school_id=sc.id))

    # Crear libros y citas (múltiples por autor)
    for i, author in enumerate(authors):
        # Obtener libros reales del autor
        author_info = AUTHOR_DATA.get(author.nombre, {})
        if isinstance(author_info, dict) and "libros" in author_info:
            author_book_list = author_info["libros"]
        else:
            author_book_list = [f"Obra de {author.nombre}"]
        
        # Crear 1-3 libros por autor
        num_books = min(len(author_book_list), random.randint(1, 3))
        selected_books = random.sample(author_book_list, num_books)
        
        for book_title in selected_books:
            # Intentar obtener portada real del libro
            cover_url = fetch_book_cover(book_title, author.nombre)
            if not cover_url:
                cover_url = book_placeholder_url(book_title)
                
            book = Book(
                titulo=book_title,
                imagen_url=cover_url,
                descripcion=f"Una obra fundamental de {author.nombre} que explora los conceptos centrales de su filosofía.",
                autor_id=author.id,
            )
            session.add(book)

        # Crear 1-2 citas por autor
        num_quotes = random.randint(1, 2)
        for _ in range(num_quotes):
            quote_text = QUOTES[random.randint(0, len(QUOTES) - 1)]
            quote = Quote(
                texto=quote_text,
                autor_id=author.id
            )
            session.add(quote)

    session.commit()


def ensure_author_images(session: Session) -> None:
    """Asigna retratos reales si es posible; si no, avatar fallback."""
    authors = session.execute(select(Author)).scalars().all()
    updated = 0
    for a in authors:
        if not a.imagen_url or "placeholder.com" in a.imagen_url or "ui-avatars.com" in a.imagen_url:
            portrait = fetch_wikipedia_portrait(a.nombre)
            a.imagen_url = portrait or author_image_url(a.nombre)
            updated += 1
    if updated:
        session.commit()


def ensure_school_images(session: Session) -> None:
    """Asigna imágenes reales de escuelas si es posible; si no, avatar fallback."""
    schools = session.execute(select(School)).scalars().all()
    updated = 0
    for s in schools:
        if not s.imagen_url or "placeholder.com" in s.imagen_url or "ui-avatars.com" in s.imagen_url:
            image = fetch_wikipedia_school_image(s.nombre)
            s.imagen_url = image or school_image_url(s.nombre)
            updated += 1
    if updated:
        session.commit()


def ensure_book_covers(session: Session) -> None:
    """Asigna portadas de libros reales si es posible; si no, placeholder personalizado."""
    books = session.execute(select(Book).join(Author)).scalars().all()
    updated = 0
    for book in books:
        if not book.imagen_url or "placeholder.com" in book.imagen_url:
            # Obtener el autor del libro
            author = session.get(Author, book.autor_id)
            if author:
                cover_url = fetch_book_cover(book.titulo, author.nombre)
                if not cover_url:
                    cover_url = book_placeholder_url(book.titulo)
                book.imagen_url = cover_url
                updated += 1
    if updated:
        session.commit()


def fix_generic_book_titles(session: Session) -> None:
    """Actualiza libros con títulos genéricos a títulos reales basados en AUTHOR_DATA."""
    books = session.execute(select(Book).join(Author)).scalars().all()
    updated = 0
    for book in books:
        # Verificar si el libro tiene un título genérico
        if book.titulo.startswith("Obra de "):
            author = session.get(Author, book.autor_id)
            if author and author.nombre in AUTHOR_DATA:
                author_info = AUTHOR_DATA[author.nombre]
                if isinstance(author_info, dict) and "libros" in author_info:
                    libros_disponibles = author_info["libros"]
                    # Asignar el primer libro disponible (o uno aleatorio)
                    import random
                    nuevo_titulo = random.choice(libros_disponibles)
                    book.titulo = nuevo_titulo
                    
                    # También actualizar la portada con el nuevo título
                    cover_url = fetch_book_cover(nuevo_titulo, author.nombre)
                    if not cover_url:
                        cover_url = book_placeholder_url(nuevo_titulo)
                    book.imagen_url = cover_url
                    
                    updated += 1
    if updated:
        session.commit()
        print(f"Actualizados {updated} libros con títulos genéricos")


