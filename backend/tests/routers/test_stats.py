import pytest
from fastapi.testclient import TestClient

from app.models import Author, School, Book, Quote


class TestStatsRouter:
    """Tests para el router de stats."""

    @pytest.mark.unit
    def test_get_stats_empty_database(self, client):
        """Test obtener estadísticas con base de datos vacía."""
        response = client.get("/stats")
        assert response.status_code == 200
        data = response.json()
        assert data["authors"] == 0
        assert data["schools"] == 0
        assert data["books"] == 0
        assert data["quotes"] == 0

    @pytest.mark.unit
    def test_get_stats_with_data(self, client, sample_author, sample_school, sample_book, sample_quote):
        """Test obtener estadísticas con datos."""
        response = client.get("/stats")
        assert response.status_code == 200
        data = response.json()
        assert data["authors"] == 1
        assert data["schools"] == 1
        assert data["books"] == 1
        assert data["quotes"] == 1

    @pytest.mark.unit
    def test_get_stats_with_multiple_data(self, client, db_session):
        """Test obtener estadísticas con múltiples registros."""
        # Crear múltiples autores
        authors = [Author(nombre=f"Autor {i}") for i in range(3)]
        for author in authors:
            db_session.add(author)

        # Crear múltiples escuelas
        schools = [School(nombre=f"Escuela {i}") for i in range(2)]
        for school in schools:
            db_session.add(school)

        db_session.commit()

        # Crear múltiples libros
        books = [
            Book(titulo=f"Libro {i}", autor_id=authors[0].id) 
            for i in range(4)
        ]
        for book in books:
            db_session.add(book)

        # Crear múltiples citas
        quotes = [
            Quote(texto=f"Cita {i}", autor_id=authors[0].id)
            for i in range(5)
        ]
        for quote in quotes:
            db_session.add(quote)

        db_session.commit()

        response = client.get("/stats")
        assert response.status_code == 200
        data = response.json()
        assert data["authors"] == 3
        assert data["schools"] == 2
        assert data["books"] == 4
        assert data["quotes"] == 5

    @pytest.mark.unit
    def test_get_random_quotes_empty_database(self, client):
        """Test obtener citas aleatorias con base de datos vacía."""
        response = client.get("/random-quotes")
        assert response.status_code == 200
        data = response.json()
        assert data == []

    @pytest.mark.unit
    def test_get_random_quotes_with_data(self, client, sample_quote, sample_author):
        """Test obtener citas aleatorias con datos."""
        response = client.get("/random-quotes")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["texto"] == "Solo sé que no sé nada"
        assert data[0]["autor_id"] == sample_author.id
        assert "id" in data[0]

    @pytest.mark.unit
    def test_get_random_quotes_with_limit(self, client, db_session):
        """Test obtener citas aleatorias con límite específico."""
        # Crear un autor
        author = Author(nombre="Autor Test")
        db_session.add(author)
        db_session.commit()

        # Crear múltiples citas
        quotes = [
            Quote(texto=f"Cita número {i}", autor_id=author.id)
            for i in range(10)
        ]
        for quote in quotes:
            db_session.add(quote)
        db_session.commit()

        # Test con límite por defecto (3)
        response = client.get("/random-quotes")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 3

        # Test con límite personalizado
        response = client.get("/random-quotes?limit=5")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 5

        # Test con límite mayor que el número de citas disponibles
        response = client.get("/random-quotes?limit=20")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 10  # Solo las 10 citas disponibles

    @pytest.mark.unit
    def test_get_random_quotes_structure(self, client, sample_quote, sample_author):
        """Test estructura de respuesta de citas aleatorias."""
        response = client.get("/random-quotes")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        
        quote = data[0]
        assert "id" in quote
        assert "texto" in quote
        assert "autor_id" in quote
        assert isinstance(quote["id"], int)
        assert isinstance(quote["texto"], str)
        assert isinstance(quote["autor_id"], int)

    @pytest.mark.unit
    def test_random_quotes_randomness(self, client, db_session):
        """Test que las citas aleatorias son realmente aleatorias."""
        # Crear un autor
        author = Author(nombre="Autor Test")
        db_session.add(author)
        db_session.commit()

        # Crear múltiples citas únicas
        quotes = [
            Quote(texto=f"Cita única número {i}", autor_id=author.id)
            for i in range(10)
        ]
        for quote in quotes:
            db_session.add(quote)
        db_session.commit()

        # Hacer múltiples peticiones y verificar que no siempre devuelve lo mismo
        responses = []
        for _ in range(10):
            response = client.get("/random-quotes?limit=3")
            assert response.status_code == 200
            data = response.json()
            texts = [quote["texto"] for quote in data]
            responses.append(tuple(sorted(texts)))

        # Verificar que hay al menos alguna variación en las respuestas
        # (Es posible que ocasionalmente sean iguales, pero muy improbable que todas sean iguales)
        unique_responses = set(responses)
        assert len(unique_responses) > 1, "Las citas aleatorias deberían variar entre peticiones"


class TestStatsIntegration:
    """Tests de integración para el router de stats."""

    @pytest.mark.integration
    def test_stats_reflect_database_changes(self, client, db_session):
        """Test que las estadísticas reflejan cambios en la base de datos."""
        # Verificar estadísticas iniciales
        response = client.get("/stats")
        initial_stats = response.json()
        assert initial_stats["authors"] == 0

        # Crear autor via API
        author_data = {"nombre": "Nuevo Autor"}
        response = client.post("/authors/", json=author_data)
        assert response.status_code == 201
        author_id = response.json()["id"]

        # Verificar que las estadísticas se actualizaron
        response = client.get("/stats")
        updated_stats = response.json()
        assert updated_stats["authors"] == 1
        assert updated_stats["schools"] == 0
        assert updated_stats["books"] == 0
        assert updated_stats["quotes"] == 0

        # Crear escuela via API
        school_data = {"nombre": "Nueva Escuela"}
        response = client.post("/schools/", json=school_data)
        assert response.status_code == 201

        # Crear libro via API
        book_data = {
            "titulo": "Nuevo Libro",
            "autor_id": author_id
        }
        response = client.post("/books/", json=book_data)
        assert response.status_code == 201

        # Crear cita via API
        quote_data = {
            "texto": "Nueva cita",
            "autor_id": author_id
        }
        response = client.post("/quotes/", json=quote_data)
        assert response.status_code == 201

        # Verificar estadísticas finales
        response = client.get("/stats")
        final_stats = response.json()
        assert final_stats["authors"] == 1
        assert final_stats["schools"] == 1
        assert final_stats["books"] == 1
        assert final_stats["quotes"] == 1

    @pytest.mark.integration
    def test_random_quotes_includes_new_quotes(self, client):
        """Test que las citas aleatorias incluyen citas recién creadas."""
        # Crear autor
        author_data = {"nombre": "Autor para citas"}
        response = client.post("/authors/", json=author_data)
        author_id = response.json()["id"]

        # Crear cita única
        unique_text = "Esta es una cita muy específica y única para el test"
        quote_data = {
            "texto": unique_text,
            "autor_id": author_id
        }
        response = client.post("/quotes/", json=quote_data)
        assert response.status_code == 201

        # Verificar que la nueva cita puede aparecer en citas aleatorias
        found_new_quote = False
        for _ in range(10):  # Intentar varias veces debido a la naturaleza aleatoria
            response = client.get("/random-quotes")
            assert response.status_code == 200
            data = response.json()
            
            for quote in data:
                if quote["texto"] == unique_text:
                    found_new_quote = True
                    break
            
            if found_new_quote:
                break

        assert found_new_quote, "La nueva cita debería aparecer en las citas aleatorias"