import pytest
from fastapi.testclient import TestClient

from app.models import Quote, Author


class TestQuotesRouter:
    """Tests para el router de quotes."""

    @pytest.mark.unit
    def test_list_quotes_empty(self, client):
        """Test listar citas cuando no hay ninguna."""
        response = client.get("/quotes/")
        assert response.status_code == 200
        assert response.json() == []

    @pytest.mark.unit
    def test_list_quotes_with_data(self, client, sample_quote, sample_author):
        """Test listar citas con datos."""
        response = client.get("/quotes/")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["texto"] == "Solo sé que no sé nada"
        assert data[0]["id"] == sample_quote.id
        assert data[0]["author"]["nombre"] == "Sócrates"

    @pytest.mark.unit
    def test_list_quotes_by_author(self, client, sample_quote, sample_author, db_session):
        """Test filtrar citas por autor."""
        # Crear otro autor y cita
        other_author = Author(nombre="Platón")
        other_quote = Quote(texto="La música es para el alma lo que la gimnasia para el cuerpo", autor_id=other_author.id)
        other_author.quotes = [other_quote]
        db_session.add(other_author)
        db_session.add(other_quote)
        db_session.commit()

        # Filtrar por el primer autor
        response = client.get(f"/quotes/?autor_id={sample_author.id}")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["texto"] == "Solo sé que no sé nada"

        # Filtrar por el segundo autor
        response = client.get(f"/quotes/?autor_id={other_author.id}")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert "música" in data[0]["texto"]

    @pytest.mark.unit
    def test_list_quotes_with_search(self, client, sample_quote):
        """Test búsqueda de citas por texto."""
        response = client.get("/quotes/?q=Solo sé")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["texto"] == "Solo sé que no sé nada"

        # Búsqueda que no encuentra nada
        response = client.get("/quotes/?q=Inexistente")
        assert response.status_code == 200
        assert response.json() == []

    @pytest.mark.unit
    def test_list_quotes_pagination(self, client, db_session):
        """Test paginación de citas."""
        # Crear un autor
        author = Author(nombre="Autor Test")
        db_session.add(author)
        db_session.commit()

        # Crear múltiples citas
        for i in range(25):
            quote = Quote(texto=f"Cita número {i}", autor_id=author.id)
            db_session.add(quote)
        db_session.commit()

        # Test primer página
        response = client.get("/quotes/?limit=10&offset=0")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 10

        # Test segunda página
        response = client.get("/quotes/?limit=10&offset=10")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 10

    @pytest.mark.unit
    def test_get_quote_success(self, client, sample_quote):
        """Test obtener una cita específica."""
        response = client.get(f"/quotes/{sample_quote.id}")
        assert response.status_code == 200
        data = response.json()
        assert data["texto"] == "Solo sé que no sé nada"
        assert data["id"] == sample_quote.id

    @pytest.mark.unit
    def test_get_quote_not_found(self, client):
        """Test obtener cita inexistente."""
        response = client.get("/quotes/99999")
        assert response.status_code == 404
        assert "Cita no encontrada" in response.json()["detail"]

    @pytest.mark.unit
    def test_create_quote_success(self, client, sample_author):
        """Test crear una nueva cita."""
        quote_data = {
            "texto": "La vida no examinada no vale la pena vivirla",
            "autor_id": sample_author.id
        }
        response = client.post("/quotes/", json=quote_data)
        assert response.status_code == 201
        data = response.json()
        assert data["texto"] == "La vida no examinada no vale la pena vivirla"
        assert data["autor_id"] == sample_author.id
        assert "id" in data

    @pytest.mark.unit
    def test_create_quote_validation_error(self, client):
        """Test crear cita con datos inválidos."""
        # Datos faltantes (texto y autor_id son requeridos)
        response = client.post("/quotes/", json={})
        assert response.status_code == 422

        # Solo texto sin autor
        response = client.post("/quotes/", json={"texto": "Cita Test"})
        assert response.status_code == 422

        # Solo autor sin texto
        response = client.post("/quotes/", json={"autor_id": 1})
        assert response.status_code == 422

    @pytest.mark.unit
    def test_create_quote_with_nonexistent_author(self, client):
        """Test crear cita con autor inexistente."""
        quote_data = {
            "texto": "Cita Test",
            "autor_id": 99999
        }
        response = client.post("/quotes/", json=quote_data)
        # La API permite crear la cita pero la relación será inválida
        # En un sistema más robusto, esto debería validar la existencia del autor
        assert response.status_code == 201

    @pytest.mark.unit
    def test_update_quote_success(self, client, sample_quote):
        """Test actualizar una cita."""
        update_data = {
            "texto": "Solo sé que no sé nada - Sócrates",
            "autor_id": sample_quote.autor_id
        }
        response = client.put(f"/quotes/{sample_quote.id}", json=update_data)
        assert response.status_code == 200
        data = response.json()
        assert data["texto"] == "Solo sé que no sé nada - Sócrates"

    @pytest.mark.unit
    def test_update_quote_not_found(self, client, sample_author):
        """Test actualizar cita inexistente."""
        update_data = {
            "texto": "Test",
            "autor_id": sample_author.id
        }
        response = client.put("/quotes/99999", json=update_data)
        assert response.status_code == 404

    @pytest.mark.unit
    def test_delete_quote_success(self, client, sample_quote):
        """Test eliminar una cita."""
        response = client.delete(f"/quotes/{sample_quote.id}")
        assert response.status_code == 204

        # Verificar que la cita ya no existe
        response = client.get(f"/quotes/{sample_quote.id}")
        assert response.status_code == 404

    @pytest.mark.unit
    def test_delete_quote_not_found(self, client):
        """Test eliminar cita inexistente."""
        response = client.delete("/quotes/99999")
        assert response.status_code == 404


class TestQuotesIntegration:
    """Tests de integración para el router de quotes."""

    @pytest.mark.integration
    def test_full_quote_workflow(self, client):
        """Test flujo completo de manejo de citas."""
        # 1. Crear autor
        author_data = {
            "nombre": "Confucio",
            "epoca": "Antigua"
        }
        response = client.post("/authors/", json=author_data)
        assert response.status_code == 201
        author_id = response.json()["id"]

        # 2. Crear cita
        quote_data = {
            "texto": "El hombre superior es modesto en el hablar y abundante en el obrar",
            "autor_id": author_id
        }
        response = client.post("/quotes/", json=quote_data)
        assert response.status_code == 201
        quote_id = response.json()["id"]

        # 3. Obtener cita creada
        response = client.get(f"/quotes/{quote_id}")
        assert response.status_code == 200
        assert "modesto" in response.json()["texto"]

        # 4. Verificar que aparece en la lista de citas
        response = client.get("/quotes/")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert "modesto" in data[0]["texto"]
        assert data[0]["author"]["nombre"] == "Confucio"

        # 5. Verificar filtrado por autor
        response = client.get(f"/quotes/?autor_id={author_id}")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert "modesto" in data[0]["texto"]

        # 6. Actualizar cita
        update_data = {
            "texto": "El hombre superior es modesto en el hablar y abundante en el obrar - Confucio",
            "autor_id": author_id
        }
        response = client.put(f"/quotes/{quote_id}", json=update_data)
        assert response.status_code == 200
        assert "Confucio" in response.json()["texto"]

        # 7. Eliminar cita
        response = client.delete(f"/quotes/{quote_id}")
        assert response.status_code == 204

        # 8. Verificar eliminación
        response = client.get(f"/quotes/{quote_id}")
        assert response.status_code == 404

    @pytest.mark.integration
    def test_quotes_search_and_filtering(self, client, db_session):
        """Test búsqueda y filtrado avanzado de citas."""
        # Crear autores
        author1 = Author(nombre="Sócrates")
        author2 = Author(nombre="Platón")
        db_session.add(author1)
        db_session.add(author2)
        db_session.commit()

        # Crear citas
        quotes = [
            Quote(texto="Solo sé que no sé nada", autor_id=author1.id),
            Quote(texto="La sabiduría comienza en el asombro", autor_id=author1.id),
            Quote(texto="La música es para el alma lo que la gimnasia para el cuerpo", autor_id=author2.id),
            Quote(texto="El primer y mejor de todos los vencedores es el que se vence a sí mismo", autor_id=author2.id)
        ]
        
        for quote in quotes:
            db_session.add(quote)
        db_session.commit()

        # Test búsqueda por texto parcial
        response = client.get("/quotes/?q=sabiduría")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert "sabiduría" in data[0]["texto"]

        # Test filtrado por autor
        response = client.get(f"/quotes/?autor_id={author1.id}")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        texts = [quote["texto"] for quote in data]
        assert any("Solo sé" in text for text in texts)
        assert any("sabiduría" in text for text in texts)

        # Test paginación
        response = client.get("/quotes/?limit=2")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2

        # Test búsqueda que encuentra múltiples resultados
        response = client.get("/quotes/?q=el")
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 2  # Varias citas contienen "el"