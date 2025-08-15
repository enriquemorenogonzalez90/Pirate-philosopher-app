from sqlalchemy.orm import Session
from .models import Author, School, Book, Quote
import random
import os
from datetime import date
import urllib.parse

# Importar S3 manager solo en producción
USE_S3 = os.getenv('USE_S3', 'false').lower() == 'true'
if USE_S3:
    try:
        from .aws_s3 import s3_manager
    except ImportError:
        USE_S3 = False
        print("⚠️ S3 no disponible, usando URLs locales")

# 200 NOMBRES EXACTOS
AUTHOR_NAMES = [
    "Sócrates", "Platón", "Aristóteles", "Epicuro", "Zenón de Citio",
    "Pitágoras", "Heráclito", "Parménides", "Diógenes", "Séneca",
    "Marco Aurelio", "Empédocles", "Anaxágoras", "Demócrito", "Epicteto",
    "Tales de Mileto", "Anaximandro", "Anaxímenes", "Jenófanes", "Protágoras",
    "Gorgias", "Antístenes", "Cleantes", "Crisipo", "Plotino",
    "Proclo", "Jámblico", "Porfirio", "Simplicio", "Alejandro de Afrodisias",
    "Filón de Alejandría", "Sexto Empírico", "Diógenes Laercio", "Apolodoro", "Hierocles",
    "Luciano de Samósata", "Galeno", "Ptolomeo", "Apolonio de Tiana", "Máximo de Tiro",
    "Confucio", "Lao Tzu", "Buda", "Nagarjuna", "Mencio",
    "Zhuangzi", "Xunzi", "Mozi", "Han Feizi", "Shankara",
    "Madhyamaka", "Asanga", "Vasubandhu", "Dignaga", "Dharmakirti",
    "Bodhidharma", "Dogen", "Nichiren", "Honen", "Shinran",
    "Basho", "Kukai", "Saicho", "Eisai", "Myoan",
    "Hakuin", "Bankei", "Ikkyu", "Ryokan", "Suzuki Daisetsu",
    "Huang Po", "Lin Chi", "Hui Neng", "Shen Xiu", "Ma Zu",
    "Zhao Zhou", "Yun Men", "Fa Yan", "Wei Yang", "Dong Shan",
    "Al-Kindi", "Al-Farabi", "Avicena", "Al-Ghazali", "Averroes",
    "Ibn Khaldun", "Al-Razi", "Ibn Sina", "Ibn Rushd", "Mulla Sadra",
    "Suhrawardi", "Ibn Arabi", "Al-Jahiz", "Al-Tabari", "Maimonides",
    "Al-Hallaj", "Ibn Taymiyyah", "Al-Ash'ari", "Al-Maturidi", "Ibn Hazm",
    "Al-Baqillani", "Al-Juwaini", "Al-Baghdadi", "Ibn Qudamah", "Al-Nawawi",
    "Ibn Qayyim", "Al-Dhahabi", "Al-Suyuti", "Ibn Hajar", "Al-Shatibi",
    "Al-Tusi", "Ibn Masarra", "Ibn Bajjah", "Ibn Tufail", "Al-Bitruji",
    "Ibn Sabʿin", "Al-Shushtari", "Ibn Qasi", "Ibn Barajan", "Al-Urfi",
    "Tomás de Aquino", "San Agustín", "Duns Escoto", "Guillermo de Ockham",
    "Anselmo de Canterbury", "Pedro Abelardo", "Juan Escoto Erígena", "Boecio",
    "Alberto Magno", "Roger Bacon", "Buenaventura", "Meister Eckhart",
    "Raimundo Lulio", "Pedro Lombardo", "Gilberto de Poitiers", "Hugo de San Víctor",
    "Ricardo de San Víctor", "Bernardo de Claraval", "Hildegarda de Bingen", "Isidoro de Sevilla",
    "Beda el Venerable", "Alcuino", "Juan Damasceno", "Máximo el Confesor", "Casiodoro",
    "Gregorio Magno", "Pseudo-Dionisio", "Juan Escoto", "Rábano Mauro", "Hincmaro de Reims",
    "Gerbert de Aurillac", "Fulberto de Chartres", "Berengario de Tours", "Lanfranco", "San Anselmo",
    "Roscelino", "Guillermo de Champeaux", "Pedro el Venerable", "Alano de Lille", "Joaquín de Fiore",
    "René Descartes", "Baruch Spinoza", "John Locke", "David Hume",
    "Immanuel Kant", "Gottfried Leibniz", "George Berkeley", "Francis Bacon",
    "Thomas Hobbes", "Voltaire", "Jean-Jacques Rousseau", "Blaise Pascal",
    "Friedrich Nietzsche", "Søren Kierkegaard", "Karl Marx", "Georg Hegel",
    "Arthur Schopenhauer", "Johann Fichte", "Friedrich Schelling", "Ludwig Wittgenstein",
    "Martin Heidegger", "Jean-Paul Sartre", "Simone de Beauvoir", "Edmund Husserl",
    "Maurice Merleau-Ponty", "Emmanuel Levinas", "Jacques Derrida", "Michel Foucault",
    "Jürgen Habermas", "Hannah Arendt", "Isaiah Berlin", "John Rawls",
    "Robert Nozick", "Alasdair MacIntyre", "Charles Taylor", "Martha Nussbaum",
    "Judith Butler", "Slavoj Žižek", "Daniel Dennett", "Thomas Nagel",
    "David Chalmers", "John Searle", "Hilary Putnam", "Saul Kripke",
    "Jerry Fodor", "Paul Churchland", "Patricia Churchland", "Andy Clark",
    "Susan Haack", "Ruth Millikan", "Fred Dretske", "Tyler Burge",
    "John Perry", "David Lewis", "Robert Stalnaker", "Bas van Fraassen",
    "Nancy Cartwright", "Ian Hacking", "Peter Galison", "Helen Longino",
    "Sandra Harding", "Donna Haraway", "Karen Barad", "Bruno Latour",
    "Michel Serres", "Paul Virilio", "Jean Baudrillard", "Gilles Deleuze",
    "Félix Guattari", "Julia Kristeva", "Hélène Cixous", "Luce Irigaray",
    "Gayatri Spivak", "Homi Bhabha", "Edward Said", "Frantz Fanon",
    "Achille Mbembe", "Enrique Dussel", "Aníbal Quijano", "Walter Mignolo",
    "Sylvia Wynter", "María Lugones", "Gloria Anzaldúa", "Audre Lorde",
    "bell hooks", "Patricia Hill Collins", "Kimberlé Crenshaw", "Angela Davis",
    "Cornel West", "Charles Mills", "José Medina", "Miranda Fricker",
    "Kristie Dotson", "Gaile Pohlhaus", "Shannon Vallor", "Luciano Floridi"
]

SCHOOL_DATA = [
    {"nombre": "Platonismo", "descripcion": "Escuela fundada por Platón."},
    {"nombre": "Aristotelismo", "descripcion": "Filosofía de Aristóteles."},
    {"nombre": "Estoicismo", "descripcion": "Escuela helenística."},
    {"nombre": "Epicureísmo", "descripcion": "Filosofía del placer."},
    {"nombre": "Existencialismo", "descripcion": "La existencia precede a la esencia."},
    {"nombre": "Fenomenología", "descripcion": "Estudio de la experiencia."},
    {"nombre": "Racionalismo", "descripcion": "Conocimiento por la razón."},
    {"nombre": "Empirismo", "descripcion": "Conocimiento por la experiencia."},
    {"nombre": "Idealismo", "descripcion": "Realidad mental."},
    {"nombre": "Materialismo", "descripcion": "Solo existe la materia."},
    {"nombre": "Utilitarismo", "descripcion": "Maximizar la felicidad."},
    {"nombre": "Deontología", "descripcion": "Ética del deber."},
    {"nombre": "Pragmatismo", "descripcion": "Verdad por consecuencias."},
    {"nombre": "Positivismo", "descripcion": "Solo conocimiento científico."},
    {"nombre": "Marxismo", "descripcion": "Filosofía de Marx."},
    {"nombre": "Feminismo", "descripcion": "Igualdad de género."},
    {"nombre": "Estructuralismo", "descripcion": "Enfoque estructural."},
    {"nombre": "Post-estructuralismo", "descripcion": "Crítica estructural."},
    {"nombre": "Hermenéutica", "descripcion": "Teoría interpretativa."},
    {"nombre": "Analítica", "descripcion": "Análisis lógico."},
    {"nombre": "Continental", "descripcion": "Tradición europea."},
    {"nombre": "Budismo", "descripcion": "Enseñanzas de Buda."},
    {"nombre": "Confucianismo", "descripcion": "Sistema ético chino."},
    {"nombre": "Taoísmo", "descripcion": "Equilibrio natural."},
    {"nombre": "Hinduismo", "descripcion": "Tradición india."},
    {"nombre": "Escolástica", "descripcion": "Filosofía medieval."},
    {"nombre": "Humanismo", "descripcion": "Dignidad humana."},
    {"nombre": "Nihilismo", "descripcion": "Negación de valores."},
    {"nombre": "Relativismo", "descripcion": "Verdad relativa."},
    {"nombre": "Absolutismo", "descripcion": "Verdades absolutas."}
]

def author_image_url(name: str) -> str:
    """Genera URL de imagen para autor (S3 en producción, UI Avatars en desarrollo)"""
    if USE_S3:
        # En producción, usar S3
        s3_key = s3_manager.generate_author_image_key(name)
        avatar_url = f"https://ui-avatars.com/api/?name={name.replace(' ', '+')}&background=random&size=300"
        
        # Subir a S3 si no existe
        if not s3_manager.file_exists(s3_key):
            s3_url = s3_manager.upload_image_from_url(avatar_url, s3_key)
            return s3_url if s3_url else avatar_url
        else:
            # Ya existe en S3 - URL encode la key
            encoded_key = urllib.parse.quote(s3_key, safe='/')
            cloudfront_domain = os.getenv('CLOUDFRONT_DOMAIN', '')
            if cloudfront_domain:
                return f"{cloudfront_domain}/{encoded_key}"
            else:
                bucket = os.getenv('S3_BUCKET_IMAGES', 'filosofia-app-images')
                return f"https://{bucket}.s3.amazonaws.com/{encoded_key}"
    else:
        # En desarrollo, usar UI Avatars directamente
        return f"https://ui-avatars.com/api/?name={name.replace(' ', '+')}&background=random&size=300"

def school_image_url(name: str) -> str:
    """Genera URL de imagen para escuela"""
    if USE_S3:
        s3_key = s3_manager.generate_school_image_key(name)
        avatar_url = f"https://ui-avatars.com/api/?name={name.replace(' ', '+')}&background=blue&color=white&size=300"
        
        if not s3_manager.file_exists(s3_key):
            s3_url = s3_manager.upload_image_from_url(avatar_url, s3_key)
            return s3_url if s3_url else avatar_url
        else:
            # URL encode la key para escuelas también
            encoded_key = urllib.parse.quote(s3_key, safe='/')
            cloudfront_domain = os.getenv('CLOUDFRONT_DOMAIN', '')
            if cloudfront_domain:
                return f"{cloudfront_domain}/{encoded_key}"
            else:
                bucket = os.getenv('S3_BUCKET_IMAGES', 'filosofia-app-images')
                return f"https://{bucket}.s3.amazonaws.com/{encoded_key}"
    else:
        return f"https://ui-avatars.com/api/?name={name.replace(' ', '+')}&background=blue&color=white&size=300"

def book_image_url(title: str, author_name: str = "") -> str:
    """Genera URL de imagen para libro"""
    if USE_S3 and author_name:
        s3_key = s3_manager.generate_book_image_key(title, author_name)
        avatar_url = f"https://ui-avatars.com/api/?name={title.replace(' ', '+')[:15]}&background=green&color=white&size=200"
        
        if not s3_manager.file_exists(s3_key):
            s3_url = s3_manager.upload_image_from_url(avatar_url, s3_key)
            return s3_url if s3_url else avatar_url
        else:
            cloudfront_domain = os.getenv('CLOUDFRONT_DOMAIN', '')
            if cloudfront_domain:
                return f"{cloudfront_domain}/{s3_key}"
            else:
                bucket = os.getenv('S3_BUCKET_IMAGES', 'filosofia-app-images')
                return f"https://{bucket}.s3.amazonaws.com/{s3_key}"
    else:
        return f"https://ui-avatars.com/api/?name={title.replace(' ', '+')[:15]}&background=green&color=white&size=200"

def seed_data_if_needed(session: Session) -> None:
    """CREAR EXACTAMENTE 200 AUTORES - ULTRA SIMPLE"""
    
    # Verificar si ya existen 200 autores
    existing = session.query(Author).count()
    print(f"🔍 SEED EJECUTÁNDOSE - Autores existentes: {existing}")
    print(f"🔍 Nombres en AUTHOR_NAMES: {len(AUTHOR_NAMES)}")
    
    if existing >= 200:
        print(f"✅ Ya existen {existing} autores")
        return

    print("🚀 FORZANDO RECREACIÓN COMPLETA...")
    
    # LIMPIAR TODO
    session.query(Quote).delete()
    session.query(Book).delete() 
    session.query(Author).delete()
    session.query(School).delete()
    session.commit()
    
    # CREAR ESCUELAS
    schools = []
    for data in SCHOOL_DATA:
        school = School(
            nombre=data["nombre"],
            imagen_url=school_image_url(data["nombre"]),
            descripcion=data["descripcion"]
        )
        session.add(school)
        schools.append(school)
    session.commit()
    print(f"✅ {len(schools)} escuelas")
    
    # CREAR 200 AUTORES
    authors = []
    for i, name in enumerate(AUTHOR_NAMES):
        if i >= 200:
            break
        
        author = Author(
            nombre=name,
            epoca="Antigua",
            fecha_nacimiento=date(300 + i, 1, 1),
            fecha_defuncion=date(350 + i, 1, 1) if i % 3 == 0 else None,
            imagen_url=author_image_url(name),
            biografia=f"{name} fue un filósofo influyente."
        )
        session.add(author)
        authors.append(author)

        # Asignar escuela
        if schools:
            author.schools.append(schools[i % len(schools)])

    session.commit()
    print(f"✅ {len(authors)} autores")

    # CREAR LIBROS SIMPLES
    for author in authors:
        book_title = f"Obras de {author.nombre}"
        book = Book(
            titulo=book_title,
            imagen_url=book_image_url(book_title, author.nombre),
            descripcion=f"Libro de {author.nombre}",
            autor_id=author.id
        )
        session.add(book)
    session.commit()
    print("✅ Libros creados")
    
    # CREAR CITAS SIMPLES
    for author in authors:
        quote = Quote(
            texto=f"Sabiduría de {author.nombre}",
            autor_id=author.id
        )
        session.add(quote)
    session.commit()
    print("✅ Citas creadas")
    
    print(f"🎉 COMPLETADO: 200 autores exactos")
