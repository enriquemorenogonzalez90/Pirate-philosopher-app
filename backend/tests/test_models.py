import pytest
from datetime import date

from app.models import Author, School, Book, Quote


class TestAuthor:
    """Tests para el modelo Author."""

    @pytest.mark.unit
    def test_create_author(self, db_session):
        """Test crear un autor básico."""
        author = Author(
            nombre="Platón",
            epoca="Antigua",
            biografia="Filósofo griego discípulo de Sócrates"
        )
        db_session.add(author)
        db_session.commit()
        
        assert author.id is not None
        assert author.nombre == "Platón"
        assert author.epoca == "Antigua"
        assert author.biografia == "Filósofo griego discípulo de Sócrates"

    @pytest.mark.unit  
    def test_author_with_dates(self, db_session):
        """Test crear autor con fechas."""
        birth_date = date(427, 1, 1)  # Año aproximado
        death_date = date(347, 1, 1)
        
        author = Author(
            nombre="Aristóteles",
            fecha_nacimiento=birth_date,
            fecha_defuncion=death_date
        )
        db_session.add(author)
        db_session.commit()
        
        assert author.fecha_nacimiento == birth_date
        assert author.fecha_defuncion == death_date

    @pytest.mark.unit
    def test_author_relationships(self, sample_author, sample_book, sample_quote, db_session):
        """Test relaciones del autor con libros y citas."""
        # El sample_author ya está en la base de datos
        # Los fixtures sample_book y sample_quote ya crean las relaciones
        
        db_session.refresh(sample_author)
        
        assert len(sample_author.books) == 1
        assert sample_author.books[0].titulo == "Apología de Sócrates"
        assert len(sample_author.quotes) == 1
        assert sample_author.quotes[0].texto == "Solo sé que no sé nada"

    @pytest.mark.unit
    def test_author_school_relationship(self, db_session):
        """Test relación many-to-many entre autor y escuela."""
        author = Author(nombre="Marco Aurelio")
        school = School(nombre="Estoicismo")
        
        author.schools.append(school)
        
        db_session.add(author)
        db_session.add(school) 
        db_session.commit()
        
        assert len(author.schools) == 1
        assert author.schools[0].nombre == "Estoicismo"
        assert len(school.authors) == 1
        assert school.authors[0].nombre == "Marco Aurelio"


class TestSchool:
    """Tests para el modelo School."""

    @pytest.mark.unit
    def test_create_school(self, db_session):
        """Test crear una escuela filosófica."""
        school = School(
            nombre="Epicureísmo",
            descripcion="Escuela filosófica helenística"
        )
        db_session.add(school)
        db_session.commit()
        
        assert school.id is not None
        assert school.nombre == "Epicureísmo"
        assert school.descripcion == "Escuela filosófica helenística"

    @pytest.mark.unit
    def test_school_with_image(self, sample_school):
        """Test escuela con imagen URL."""
        assert sample_school.imagen_url == "https://example.com/stoicism.jpg"

    @pytest.mark.unit
    def test_school_authors_relationship(self, sample_school, db_session):
        """Test relación escuela con autores."""
        author1 = Author(nombre="Séneca")
        author2 = Author(nombre="Epicteto")
        
        sample_school.authors.append(author1)
        sample_school.authors.append(author2)
        
        db_session.add(author1)
        db_session.add(author2)
        db_session.commit()
        
        assert len(sample_school.authors) == 2
        assert author1 in sample_school.authors
        assert author2 in sample_school.authors


class TestBook:
    """Tests para el modelo Book."""

    @pytest.mark.unit
    def test_create_book(self, sample_author, db_session):
        """Test crear un libro."""
        book = Book(
            titulo="La República",
            autor_id=sample_author.id,
            descripcion="Obra maestra de filosofía política"
        )
        db_session.add(book)
        db_session.commit()
        
        assert book.id is not None
        assert book.titulo == "La República"
        assert book.autor_id == sample_author.id

    @pytest.mark.unit
    def test_book_author_relationship(self, sample_book, sample_author):
        """Test relación libro con autor."""
        assert sample_book.author == sample_author
        assert sample_book.autor_id == sample_author.id

    @pytest.mark.unit
    def test_book_with_image(self, sample_book):
        """Test libro con imagen URL."""
        assert sample_book.imagen_url == "https://example.com/book.jpg"


class TestQuote:
    """Tests para el modelo Quote."""

    @pytest.mark.unit
    def test_create_quote(self, sample_author, db_session):
        """Test crear una cita."""
        quote = Quote(
            texto="La vida no examinada no vale la pena vivirla",
            autor_id=sample_author.id
        )
        db_session.add(quote)
        db_session.commit()
        
        assert quote.id is not None
        assert quote.texto == "La vida no examinada no vale la pena vivirla"
        assert quote.autor_id == sample_author.id

    @pytest.mark.unit
    def test_quote_author_relationship(self, sample_quote, sample_author):
        """Test relación cita con autor."""
        assert sample_quote.author == sample_author
        assert sample_quote.autor_id == sample_author.id

    @pytest.mark.unit
    def test_quote_required_fields(self, db_session):
        """Test que los campos requeridos están presentes."""
        quote = Quote(texto="", autor_id=1)
        db_session.add(quote)
        
        # Este test verificará que el texto no puede estar vacío
        # En un modelo más estricto, esto debería fallar
        db_session.commit()
        assert quote.texto == ""  # Por ahora acepta strings vacíos


class TestModelIntegration:
    """Tests de integración entre modelos."""

    @pytest.mark.integration
    def test_complete_philosopher_data(self, db_session):
        """Test crear un filósofo completo con todas las relaciones."""
        # Crear autor
        author = Author(
            nombre="Immanuel Kant",
            epoca="Moderna",
            biografia="Filósofo alemán de la Ilustración"
        )
        
        # Crear escuela
        school = School(
            nombre="Idealismo Alemán",
            descripcion="Corriente filosófica alemana"
        )
        
        # Crear libro
        book = Book(
            titulo="Crítica de la Razón Pura",
            descripcion="Obra fundamental del criticismo kantiano"
        )
        
        # Crear cita
        quote = Quote(
            texto="Actúa solo según aquella máxima que puedas querer que se convierta en ley universal"
        )
        
        # Establecer relaciones
        author.schools.append(school)
        book.author = author
        quote.author = author
        
        # Guardar en base de datos
        db_session.add(author)
        db_session.add(school)
        db_session.add(book)
        db_session.add(quote)
        db_session.commit()
        
        # Verificar que todo se guardó correctamente
        assert author.id is not None
        assert school.id is not None
        assert book.id is not None
        assert quote.id is not None
        
        # Verificar relaciones
        assert len(author.schools) == 1
        assert len(author.books) == 1
        assert len(author.quotes) == 1
        assert school.authors[0] == author
        assert book.author == author
        assert quote.author == author