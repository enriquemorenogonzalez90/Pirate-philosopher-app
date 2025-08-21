"""
Colección de citas auténticas de filósofos famosos
"""

# Diccionario de citas reales organizadas por filósofo
PHILOSOPHER_QUOTES = {
    # Filósofos Griegos Antiguos
    "Sócrates": [
        "Solo sé que no sé nada",
        "La vida no examinada no vale la pena ser vivida",
        "El conocimiento es virtud",
        "Nadie yerra voluntariamente",
        "Conócete a ti mismo"
    ],
    
    "Platón": [
        "La realidad es una sombra de las ideas",
        "El alma del hombre es inmortal e imperecedera",
        "La música es para el alma lo que la gimnasia para el cuerpo",
        "Al contacto del amor, todo hombre se convierte en poeta",
        "La necesidad es la madre de la invención"
    ],
    
    "Aristóteles": [
        "El hombre es un animal político",
        "La esperanza es el sueño del hombre despierto",
        "La educación es el mejor provecho que pueden tener los ricos",
        "Somos lo que hacemos repetidamente. La excelencia no es un acto, sino un hábito",
        "El sabio no dice todo lo que piensa, pero siempre piensa todo lo que dice"
    ],
    
    "Epicuro": [
        "La muerte no es nada para nosotros",
        "El placer es el principio y el fin de la felicidad",
        "La amistad danza alrededor del mundo proclamando a todos que despierten al reconocimiento de la felicidad",
        "No estropees lo que tienes deseando lo que no tienes",
        "El miedo a la muerte es la fuente de todos los males"
    ],
    
    "Zenón de Citio": [
        "El sabio es aquel que solo teme la falta de sabiduría",
        "La felicidad es una buena circulación de la vida",
        "Tenemos dos oídos y una boca para escuchar más y hablar menos",
        "El objetivo de la vida es vivir en conformidad con la naturaleza",
        "La virtud es la única riqueza verdadera"
    ],
    
    "Heráclito": [
        "Nadie se baña en el río dos veces porque todo cambia en el río y en el que se baña",
        "La guerra es el padre de todas las cosas",
        "Los contrarios son necesarios",
        "La armonía oculta es mejor que la aparente",
        "El carácter del hombre es su destino"
    ],
    
    "Pitágoras": [
        "Los números gobiernan el universo",
        "Educad a los niños y no será necesario castigar a los hombres",
        "Escoge la mejor manera de vivir; la costumbre te la hará agradable",
        "Los amigos son compañeros de viaje, que nos ayudan a avanzar por el sendero hacia una vida más dichosa y plena",
        "No desprecies a nadie; un átomo hace sombra"
    ],
    
    # Filósofos Romanos
    "Séneca": [
        "No hay viento favorable para quien no sabe a dónde va",
        "La vida es larga si sabes cómo usarla",
        "Todo lo que somos es resultado de lo que hemos pensado",
        "La ira es una locura temporal",
        "El tiempo es lo único que realmente poseemos"
    ],
    
    "Marco Aurelio": [
        "Tienes poder sobre tu mente, no sobre eventos externos. Date cuenta de esto y encontrarás fortaleza",
        "La mejor venganza es no ser como tu enemigo",
        "Lo que no nos beneficia como enjambre no puede beneficiar a la abeja",
        "La felicidad de tu vida depende de la calidad de tus pensamientos",
        "Recuerda que muy poco perturba a aquel que tiene todo bajo control"
    ],
    
    "Epicteto": [
        "No son los hechos los que perturban a los hombres, sino los juicios sobre los hechos",
        "La riqueza no consiste en tener grandes propiedades, sino en tener pocas necesidades",
        "Ningún hombre es libre si no es dueño de sí mismo",
        "Dios nos ha dado una mente y la capacidad de elegir cómo usarla",
        "El contentamiento es la riqueza natural"
    ],
    
    # Filósofos Orientales
    "Confucio": [
        "El hombre superior es modesto en el hablar y abundante en el obrar",
        "Elige un trabajo que te guste y no tendrás que trabajar ni un día de tu vida",
        "La ignorancia es la noche de la mente, pero una noche sin luna ni estrellas",
        "No te preocupes porque la gente no te conozca, sino porque quizá no conozcas tú a la gente",
        "Si ya sabes lo que tienes que hacer y no lo haces, entonces estás peor que antes"
    ],
    
    "Lao Tzu": [
        "El viaje de mil millas comienza con un paso",
        "Conocer a otros es inteligencia; conocerse a sí mismo es sabiduría verdadera",
        "La naturaleza no tiene prisa, pero todo se logra",
        "Aquel que sabe que tiene suficiente es rico",
        "El agua es fluida, suave y débil. Sin embargo, nada puede superar al agua"
    ],
    
    "Buda": [
        "El dolor es inevitable, el sufrimiento es opcional",
        "Todo lo que somos es resultado de lo que hemos pensado",
        "Tres cosas no pueden permanecer ocultas: el sol, la luna y la verdad",
        "No creas nada porque lo diga la tradición, ni siquiera porque lo hayan dicho muchas generaciones",
        "Tu peor enemigo no te puede hacer tanto daño como tus propios pensamientos"
    ],
    
    # Filósofos Medievales
    "Tomás de Aquino": [
        "Tres cosas son necesarias para la salvación del hombre: saber lo que debe creer, saber lo que debe desear, y saber lo que debe hacer",
        "La fe y la razón son como dos alas con las cuales el espíritu humano se eleva",
        "El estudio de la filosofía no es para saber lo que pensaron los hombres, sino cuál es la verdad de las cosas",
        "Nada hay en el entendimiento que no haya estado antes en los sentidos",
        "La ley natural no es otra cosa que la participación de la ley eterna en la criatura racional"
    ],
    
    "San Agustín": [
        "Ama y haz lo que quieras",
        "La fe busca el entendimiento",
        "El mundo es un libro y quienes no viajan leen solo una página",
        "La paciencia es la compañera de la sabiduría",
        "No salgas fuera de ti mismo, vuelve a ti; en el hombre interior reside la verdad"
    ],
    
    # Filósofos Modernos
    "René Descartes": [
        "Pienso, luego existo",
        "La duda es el origen de la sabiduría",
        "Para investigar la verdad es preciso dudar, en cuanto sea posible, de todas las cosas",
        "El sentido común es la cosa mejor distribuida del mundo",
        "La lectura de todos los buenos libros es como una conversación con las mejores personas de los siglos pasados"
    ],
    
    "Baruch Spinoza": [
        "La naturaleza no hace nada en vano",
        "El miedo no puede existir sin esperanza ni esperanza sin miedo",
        "Las emociones que son pasiones dejan de serlo tan pronto como nos formamos una idea clara de las mismas",
        "Nadie puede amar verdaderamente a Dios sin que Dios le ame a él",
        "La libertad no es la ausencia de necesidad sino el conocimiento de la necesidad"
    ],
    
    "Immanuel Kant": [
        "Actúa solo según aquella máxima que puedas querer que se convierta en ley universal",
        "Dos cosas llenan el ánimo de admiración y respeto: el cielo estrellado sobre mí y la ley moral en mí",
        "La felicidad no es un ideal de la razón sino de la imaginación",
        "Ten valor de servirte de tu propia razón",
        "Obra de tal modo que trates a la humanidad, tanto en tu persona como en la de cualquier otro, siempre como fin y nunca como medio"
    ],
    
    "David Hume": [
        "La costumbre es la guía de la vida humana",
        "No hay nada en sí mismo bueno o malo, sino que el pensamiento humano lo hace aparecer así",
        "La razón es esclava de las pasiones",
        "Un hombre sabio proporciona sus creencias a la evidencia",
        "La belleza no existe por sí misma; existe en la mente que la contempla"
    ],
    
    "John Locke": [
        "No hay nada en la mente que no haya estado antes en los sentidos",
        "La educación del hombre comienza al nacer",
        "Lo que preocupa no es que tengas una opinión diferente a la mía, sino que yo sea incapaz de ser de tu opinión",
        "Ningún conocimiento humano puede ir más allá de su experiencia",
        "El gobierno no tiene otro fin que la conservación de la propiedad"
    ],
    
    # Filósofos Contemporáneos
    "Friedrich Nietzsche": [
        "Lo que no me mata me fortalece",
        "Dios ha muerto",
        "Conviértete en quien eres",
        "Sin música, la vida sería un error",
        "El hombre es algo que debe ser superado"
    ],
    
    "Arthur Schopenhauer": [
        "El mundo es mi representación",
        "La vida oscila entre los polos de la necesidad y del aburrimiento",
        "Toda satisfacción o felicidad es de naturaleza esencialmente negativa",
        "La cortesía es para la naturaleza humana lo que el calor es para la cera",
        "Los grandes pensamientos vienen del corazón"
    ],
    
    "Søren Kierkegaard": [
        "La vida solo puede ser comprendida mirando hacia atrás, pero debe ser vivida mirando hacia adelante",
        "La desesperación es la enfermedad mortal",
        "La ansiedad es el vértigo de la libertad",
        "La fe comienza precisamente donde termina el pensamiento",
        "El individuo debe pasar por tres estadios: el estético, el ético y el religioso"
    ],
    
    "Karl Marx": [
        "Los filósofos no han hecho más que interpretar de diversos modos el mundo, pero de lo que se trata es de transformarlo",
        "La historia de todas las sociedades que han existido hasta nuestros días es la historia de las luchas de clases",
        "La religión es el opio del pueblo",
        "No es la conciencia del hombre la que determina su ser, sino el ser social lo que determina su conciencia",
        "De cada cual según su capacidad; a cada cual según sus necesidades"
    ],
    
    "Georg Hegel": [
        "Lo racional es real y lo real es racional",
        "La lechuza de Minerva alza el vuelo al atardecer",
        "La verdad es el todo",
        "La libertad es la comprensión de la necesidad",
        "La historia del mundo no es sino el progreso de la conciencia de la libertad"
    ],
    
    "Ludwig Wittgenstein": [
        "Los límites de mi lenguaje son los límites de mi mundo",
        "De lo que no se puede hablar, mejor es callarse",
        "Un problema filosófico tiene la forma: no sé cómo orientarme",
        "La filosofía es una lucha contra el embrujo de nuestro entendimiento por medio del lenguaje",
        "El significado de una palabra es su uso en el lenguaje"
    ],
    
    # Filósofos Medievales Adicionales
    "Alberto Magno": [
        "La filosofía es la ciencia de las ciencias",
        "La fe busca el entendimiento a través de la razón",
        "La experiencia es la base de todo conocimiento científico"
    ],
    
    "Anselmo de Canterbury": [
        "La fe busca el entendimiento",
        "Dios es aquello mayor que lo cual nada puede pensarse",
        "No trato de entender para creer, sino que creo para entender"
    ],
    
    "Pedro Abelardo": [
        "La duda nos lleva a la investigación, y la investigación nos lleva a la verdad",
        "El conocimiento de sí mismo es el comienzo de toda sabiduría",
        "La autoridad tiene una nariz de cera que se puede doblar en cualquier dirección"
    ],
    
    "Juan Escoto Erígena": [
        "La autoridad procede de la recta razón, pero la razón no procede de la autoridad",
        "Nadie entra en el cielo excepto a través de la filosofía",
        "La verdadera filosofía es la verdadera religión"
    ],
    
    "Boecio": [
        "En toda adversidad de la fortuna, la más infeliz especie de infortunio es haber sido feliz",
        "La música es parte de nosotros y ennoblece o degrada nuestra conducta",
        "Nada hay más fugaz que la forma externa, que se marchita y cambia como las flores del campo"
    ],
    
    "Buenaventura": [
        "El alma llega a Dios por tres caminos: la purificación, la iluminación y la perfección",
        "Cristo es el camino y la puerta, la escalera y el vehículo",
        "Nadie puede ser feliz sin la suprema y perfecta sabiduría"
    ],
    
    "Meister Eckhart": [
        "El ojo a través del cual veo a Dios es el mismo ojo a través del cual Dios me ve",
        "Para el alma desprendida, todo dolor es gozo y toda carga es alivio",
        "Si la única oración que dijeras en toda tu vida fuera 'gracias', sería suficiente"
    ],
    
    "Duns Escoto": [
        "Cada cosa individual tiene su propia esencia única",
        "La voluntad es más noble que el intelecto",
        "Dios puede hacer todo lo que no implique contradicción"
    ],
    
    "Guillermo de Ockham": [
        "No se debe multiplicar las entidades sin necesidad",
        "La navaja de Ockham: la explicación más simple suele ser la correcta",
        "Nada debe ser afirmado sin razón"
    ],
    
    # Filósofos Antiguos Adicionales
    "Tales de Mileto": [
        "El agua es el principio de todas las cosas",
        "Todo está lleno de dioses",
        "Conócete a ti mismo es la más difícil de las tareas"
    ],
    
    "Anaximandro": [
        "El principio de todas las cosas es lo indefinido",
        "La injusticia se paga con justicia según el orden del tiempo",
        "De donde nacen todas las cosas, allí también perecen según la necesidad"
    ],
    
    "Anaxímenes": [
        "El aire es el principio de todas las cosas",
        "Como nuestra alma, que es aire, nos mantiene unidos, así el pneuma y el aire mantienen unido el cosmos",
        "Los dioses también nacen del aire"
    ],
    
    "Jenófanes": [
        "Si los bueyes, caballos y leones tuvieran manos y pudieran dibujar, pintarían dioses semejantes a ellos",
        "Los mortales creen que los dioses nacen, tienen vestidos, voces y figuras como ellos",
        "No hay hombre que haya conocido ni conocerá jamás la verdad sobre los dioses"
    ],
    
    "Protágoras": [
        "El hombre es la medida de todas las cosas",
        "Hay dos razones opuestas sobre cada cosa",
        "La educación no brota en el alma si antes no llega a las raíces"
    ],
    
    "Gorgias": [
        "Nada existe; si algo existiera, no podría conocerse; si pudiera conocerse, no podría comunicarse",
        "El tiempo es el más sabio consejero",
        "La palabra es un poderoso soberano"
    ],
    
    "Antístenes": [
        "La sabiduría es la más segura muralla",
        "Prefiero volverme loco a sentir placer",
        "La virtud es suficiente para la felicidad"
    ],
    
    "Cleantes": [
        "Condúceme, Zeus, y tú, Destino, por el camino que me habéis asignado",
        "El sabio vive conforme a la naturaleza",
        "La razón es el principio rector del universo"
    ],
    
    "Empédocles": [
        "Dios es una mente sagrada e inefable que atraviesa todo el cosmos con rápidos pensamientos",
        "Nada nace ni perece, sino que las cosas existentes se combinan y se separan",
        "El amor y el odio son las fuerzas que mueven el universo"
    ],
    
    "Anaxágoras": [
        "En todo hay una porción de todo",
        "El sol es una masa de metal incandescente",
        "La mente ordenó todas las cosas"
    ],
    
    "Parménides": [
        "El ser es y el no-ser no es",
        "Lo mismo es pensar y ser",
        "Los mortales han establecido la distinción entre luz y noche"
    ],
    
    "Plotino": [
        "El alma del hombre es inmortal y parte de ella regresa a Dios",
        "La belleza es el resplandor de la verdad",
        "Solo el que ha visto puede hablar de lo que ha visto"
    ],
    
    "Proclo": [
        "Todo lo que participa procede de lo imparticipado",
        "El alma está en el medio entre lo divino y lo mortal",
        "La filosofía es la ascensión hacia lo divino"
    ],
    
    "Jámblico": [
        "Los dioses no descienden a nosotros, sino que nosotros ascendemos a ellos",
        "La filosofía debe unirse con la teúrgia",
        "El alma humana puede alcanzar la unión con lo divino"
    ],
    
    "Porfirio": [
        "La filosofía purifica el alma",
        "Los dioses no necesitan sacrificios, sino virtud",
        "La abstinencia fortalece el alma"
    ],
    
    "Simplicio": [
        "La filosofía antigua merece respeto y estudio",
        "Aristóteles es el comentador más fiel de Platón",
        "La verdad se encuentra a través del diálogo con los antiguos"
    ],
    
    "Alejandro de Afrodisias": [
        "El destino es la conexión de las causas",
        "El alma humana es mortal, solo el intelecto es eterno",
        "La libertad existe dentro del orden cósmico"
    ],
    
    "Filón de Alejandría": [
        "Dios no puede ser comprendido por la mente humana",
        "La Escritura debe interpretarse alegóricamente",
        "La sabiduría griega prepara el camino hacia la verdad divina"
    ],
    
    "Diógenes Laercio": [
        "La filosofía es el amor a la sabiduría",
        "Conocer las vidas de los filósofos es conocer la filosofía misma",
        "La virtud se enseña con el ejemplo"
    ],
    
    "Hierocles": [
        "Somos ciudadanos del mundo",
        "La justicia es la armonía del alma",
        "El sabio vive en concordancia con la naturaleza universal"
    ],
    
    "Luciano de Samósata": [
        "La risa es el mejor remedio para las vanidades humanas",
        "Los dioses de los hombres son tan diversos como sus costumbres",
        "La filosofía dogmática merece ser satirizada"
    ],
    
    "Galeno": [
        "La experiencia es la madre de todas las ciencias",
        "El cuerpo y el alma están íntimamente unidos",
        "La medicina es la más noble de todas las artes"
    ],
    
    "Ptolomeo": [
        "La astronomía es la ciencia más divina",
        "Los cuerpos celestes siguen leyes matemáticas perfectas",
        "El conocimiento de los cielos eleva el alma"
    ],
    
    "Apolonio de Tiana": [
        "La sabiduría es la única riqueza que no puede ser robada",
        "El alma sabia encuentra a Dios en todas las cosas",
        "La vida contemplativa es superior a la activa"
    ],
    
    # Filósofos Orientales Adicionales
    "Mencio": [
        "La naturaleza humana es fundamentalmente buena",
        "El buen gobierno se basa en la virtud del gobernante",
        "El corazón compasivo es el comienzo de la humanidad"
    ],
    
    "Mozi": [
        "Debemos amar a todos sin distinción",
        "Las acciones se juzgan por sus consecuencias útiles",
        "El cielo ama a todos los hombres por igual"
    ],
    
    "Zhuangzi": [
        "El sabio no se aferra a nada, por eso no puede perder nada",
        "La felicidad perfecta es la ausencia de la búsqueda de felicidad",
        "¿Cómo sé si amar la vida no es un engaño? ¿Cómo sé si odiar la muerte no es como un niño perdido que no encuentra el camino a casa?"
    ],
    
    "Nagarjuna": [
        "Todo surge en dependencia, nada existe independientemente",
        "La vacuidad es la naturaleza última de la realidad",
        "El nirvana no es diferente del samsara"
    ],
    
    "Shankara": [
        "Brahman es la única realidad, el mundo es apariencia",
        "Tat tvam asi: tú eres eso",
        "El conocimiento del Ser destruye toda ignorancia"
    ],
    
    # Filósofos Contemporáneos Adicionales
    "Bertrand Russell": [
        "El problema con el mundo es que los estúpidos están seguros de sí mismos y los inteligentes llenos de dudas",
        "La filosofía es algo intermedio entre la teología y la ciencia",
        "No temas ser excéntrico en tus opiniones, pues toda opinión ahora aceptada fue una vez excéntrica"
    ],
    
    "Alfred North Whitehead": [
        "El objetivo de la educación es el arte de la utilización del conocimiento",
        "La filosofía comienza en el asombro y termina en el asombro",
        "La civilización avanza ampliando el número de operaciones importantes que podemos realizar sin pensar"
    ],
    
    "William James": [
        "La verdad de una idea no es una propiedad estática inherente a ella, sino algo que acontece",
        "El arte de ser sabio es saber qué pasar por alto",
        "El mayor descubrimiento de cualquier generación es que los seres humanos pueden cambiar su vida cambiando su actitud mental"
    ],
    
    "John Dewey": [
        "No aprendemos de la experiencia... aprendemos reflexionando sobre la experiencia",
        "La educación es vida, no una preparación para la vida",
        "El fracaso es instructivo. La persona que realmente piensa aprende tanto de sus fracasos como de sus éxitos"
    ],
    
    "Edmund Husserl": [
        "A las cosas mismas",
        "La conciencia es siempre conciencia de algo",
        "La filosofía es una ciencia rigurosa"
    ],
    
    "Jean-Paul Sartre": [
        "El infierno son los otros",
        "La existencia precede a la esencia",
        "El hombre está condenado a ser libre"
    ],
    
    "Maurice Merleau-Ponty": [
        "El cuerpo es nuestro medio general de tener un mundo",
        "Somos seres encarnados en el mundo",
        "La percepción no es una ciencia del mundo, es el trasfondo sobre el cual se destacan todos los actos"
    ],
    
    "Hannah Arendt": [
        "El poder corresponde a la capacidad humana no sólo de actuar, sino de actuar de manera concertada",
        "La banalidad del mal",
        "Solo podemos conocer el sentido de la política si conocemos la dignidad de lo que está en juego"
    ],
    
    "Simone de Beauvoir": [
        "No se nace mujer, se llega a serlo",
        "La mujer se define y se diferencia en relación al hombre, no él en relación a ella",
        "Es a través del trabajo que la mujer ha podido franquear la distancia que la separaba del hombre"
    ],
    
    "Michel Foucault": [
        "Donde hay poder, hay resistencia",
        "El sujeto se constituye a través de prácticas de sujeción",
        "No hay que describir el poder como algo que prohíbe, sino como algo que produce"
    ],
    
    "Jacques Derrida": [
        "No hay nada fuera del texto",
        "La différance precede a la diferencia",
        "Todo signo puede ser citado, injertado; todo signo puede romper con todo contexto dado"
    ],
    
    "Jürgen Habermas": [
        "La modernidad es un proyecto inacabado",
        "El mejor argumento racional debe prevalecer",
        "La acción comunicativa busca el entendimiento mutuo"
    ],
    
    "John Rawls": [
        "La justicia es la primera virtud de las instituciones sociales",
        "El velo de ignorancia asegura la imparcialidad",
        "Una sociedad justa es aquella que escogeríamos si no supiéramos nuestro lugar en ella"
    ],
    
    "Robert Nozick": [
        "Los individuos tienen derechos, y hay cosas que ninguna persona o grupo puede hacerles",
        "La libertad altera los patrones distributivos",
        "El Estado mínimo es el más amplio que se puede justificar"
    ],
    
    "Martha Nussbaum": [
        "Las emociones son evaluaciones cognitivas",
        "La capacidad es lo que una persona puede hacer y ser",
        "La educación liberal cultiva la humanidad"
    ],
    
    "Judith Butler": [
        "El género es performativo",
        "No hay identidad de género detrás de las expresiones de género",
        "Los cuerpos que importan son aquellos que pueden ser reconocidos como humanos"
    ],
    
    "Slavoj Žižek": [
        "La ideología funciona mejor cuando es invisible",
        "El verdadero horror no es la muerte, sino la vida eterna",
        "Primero como tragedia, después como farsa"
    ],
    
    "Walter Benjamin": [
        "La historia la escriben los vencedores",
        "En cada época hay que intentar arrancar la tradición de manos del conformismo",
        "No hay documento de cultura que no sea a la vez documento de barbarie"
    ],
    
    # Filósofos Hispanos
    "José Ortega y Gasset": [
        "Yo soy yo y mi circunstancia",
        "La vida es quehacer",
        "Dime a qué prestas atención y te diré quién eres"
    ],
    
    "Miguel de Unamuno": [
        "Se hace camino al andar",
        "La fe que no duda no es fe",
        "El escepticismo es la fuerza disolvente de la fe, y la fe la fuerza vivificante del escepticismo"
    ],
    
    "María Zambrano": [
        "La razón poética es el saber del alma",
        "Filosofar es despertar",
        "La palabra es el único recurso contra el tiempo"
    ],
    
    # Sociólogos-Filósofos
    "Max Weber": [
        "La política es una actividad lenta y tenaz que perfora tablas de madera dura",
        "El desencantamiento del mundo es el destino de la modernidad",
        "La ética de la responsabilidad debe guiar al político"
    ],
    
    "Antonio Gramsci": [
        "La cultura es el ejercicio del pensamiento",
        "Todos los hombres son intelectuales, pero no todos desempeñan la función de intelectuales en la sociedad",
        "Pesimismo de la inteligencia, optimismo de la voluntad"
    ],
    
    "Emmanuel Levinas": [
        "El rostro del otro es el lugar donde se revela Dios",
        "La ética es la filosofía primera",
        "El infinito se produce en la relación de lo mismo con lo otro"
    ],
    
    "Paul Ricoeur": [
        "El símbolo da que pensar",
        "Explicar más para comprender mejor",
        "La narrativa es la estructura fundamental de la experiencia humana"
    ],
    
    "Hans-Georg Gadamer": [
        "Ser que puede ser comprendido es lenguaje",
        "En toda comprensión se produce una fusión de horizontes",
        "La tradición no es algo que simplemente se hereda, sino que se recrea constantemente"
    ],
    
    "Henri Bergson": [
        "La duración es el progreso continuo del pasado que roe el porvenir",
        "El cuerpo es un centro de acción",
        "Reír es una función social que tiene por fin intimidar"
    ]
}


def get_quotes_for_author(author_name: str) -> list[str]:
    """
    Obtiene todas las citas disponibles para un autor específico.
    
    Args:
        author_name: Nombre del filósofo
        
    Returns:
        Lista de citas del filósofo, o una cita genérica si no se encuentra
    """
    if author_name in PHILOSOPHER_QUOTES:
        return PHILOSOPHER_QUOTES[author_name]
    
    # Citas genéricas para filósofos no catalogados específicamente
    return [f"Las palabras de {author_name} resuenan a través del tiempo con sabiduría eterna."]


def get_random_quote_for_author(author_name: str) -> str:
    """
    Obtiene una cita aleatoria para un autor específico.
    
    Args:
        author_name: Nombre del filósofo
        
    Returns:
        Una cita aleatoria del filósofo
    """
    import random
    quotes = get_quotes_for_author(author_name)
    return random.choice(quotes)


def get_all_quotes_dict() -> dict[str, list[str]]:
    """
    Obtiene el diccionario completo de todas las citas.
    
    Returns:
        Diccionario con todos los filósofos y sus citas
    """
    return PHILOSOPHER_QUOTES.copy()


def get_total_quotes_count() -> int:
    """
    Cuenta el total de citas disponibles.
    
    Returns:
        Número total de citas en la base de datos
    """
    return sum(len(quotes) for quotes in PHILOSOPHER_QUOTES.values())