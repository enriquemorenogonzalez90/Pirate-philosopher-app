import pytest
from fastapi.testclient import TestClient

from app.models import Author, School


class TestAuthorsRouter:
    """Tests para el router de authors."""

    @pytest.mark.unit
    def test_list_authors_empty(self, client):
        """Test listar autores cuando no hay ninguno."""
        response = client.get("/authors/")
        assert response.status_code == 200
        assert response.json() == []

    @pytest.mark.unit  
    def test_list_authors_with_data(self, client, sample_author):
        """Test listar autores con datos."""
        response = client.get("/authors/")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["nombre"] == "Sócrates"
        assert data[0]["epoca"] == "Antigua"
        assert data[0]["id"] == sample_author.id

    @pytest.mark.unit
    def test_list_authors_with_search(self, client, sample_author):
        """Test búsqueda de autores por nombre."""
        response = client.get("/authors/?q=Sócr")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["nombre"] == "Sócrates"

        # Búsqueda que no encuentra nada
        response = client.get("/authors/?q=Platón")
        assert response.status_code == 200
        assert response.json() == []

    @pytest.mark.unit
    def test_list_authors_by_epoca(self, client, sample_author, db_session):
        """Test filtrado de autores por época."""
        # Crear autor de diferente época
        modern_author = Author(nombre="Kant", epoca="Moderna")
        db_session.add(modern_author)
        db_session.commit()

        # Filtrar por época antigua
        response = client.get("/authors/?epoca=Antigua")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["nombre"] == "Sócrates"

        # Filtrar por época moderna  
        response = client.get("/authors/?epoca=Moderna")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["nombre"] == "Kant"

    @pytest.mark.unit
    def test_list_authors_pagination(self, client, db_session):
        """Test paginación de autores."""
        # Crear múltiples autores
        for i in range(25):
            author = Author(nombre=f"Autor {i}")
            db_session.add(author)
        db_session.commit()

        # Test primer página
        response = client.get("/authors/?limit=10&offset=0")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 10

        # Test segunda página
        response = client.get("/authors/?limit=10&offset=10")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 10

        # Test límite máximo
        response = client.get("/authors/?limit=200")
        assert response.status_code == 422  # Validation error

    @pytest.mark.unit
    def test_list_authors_sorting(self, client, db_session):
        """Test ordenamiento de autores."""
        # Crear autores en orden específico
        authors = [
            Author(nombre="Zebra"),
            Author(nombre="Alpha"),
            Author(nombre="Beta")
        ]
        for author in authors:
            db_session.add(author)
        db_session.commit()

        # Test orden ascendente por nombre
        response = client.get("/authors/?sort=nombre")
        assert response.status_code == 200
        data = response.json()
        names = [author["nombre"] for author in data]
        assert names == ["Alpha", "Beta", "Zebra"]

        # Test orden descendente por nombre
        response = client.get("/authors/?sort=-nombre")
        assert response.status_code == 200
        data = response.json()
        names = [author["nombre"] for author in data]
        assert names == ["Zebra", "Beta", "Alpha"]

    @pytest.mark.unit
    def test_get_author_success(self, client, sample_author):
        """Test obtener un autor específico."""
        response = client.get(f"/authors/{sample_author.id}")
        assert response.status_code == 200
        data = response.json()
        assert data["nombre"] == "Sócrates"
        assert data["id"] == sample_author.id
        assert "schools" in data
        assert "books" in data

    @pytest.mark.unit
    def test_get_author_not_found(self, client):
        """Test obtener autor inexistente."""
        response = client.get("/authors/99999")
        assert response.status_code == 404
        assert "Autor no encontrado" in response.json()["detail"]

    @pytest.mark.unit
    def test_create_author_success(self, client):
        """Test crear un nuevo autor."""
        author_data = {
            "nombre": "Aristóteles",
            "epoca": "Antigua",
            "biografia": "Discípulo de Platón y tutor de Alejandro Magno"
        }
        response = client.post("/authors/", json=author_data)
        assert response.status_code == 201
        data = response.json()
        assert data["nombre"] == "Aristóteles"
        assert data["epoca"] == "Antigua" 
        assert "id" in data

    @pytest.mark.unit
    def test_create_author_validation_error(self, client):
        """Test crear autor con datos inválidos."""
        # Datos faltantes (nombre es requerido)
        response = client.post("/authors/", json={})
        assert response.status_code == 422

        # Nombre vacío
        response = client.post("/authors/", json={"nombre": ""})
        assert response.status_code == 422

    @pytest.mark.unit
    def test_update_author_success(self, client, sample_author):
        """Test actualizar un autor."""
        update_data = {
            "nombre": "Sócrates el Grande",
            "epoca": "Clásica",
            "biografia": "Biografía actualizada"
        }
        response = client.put(f"/authors/{sample_author.id}", json=update_data)
        assert response.status_code == 200
        data = response.json()
        assert data["nombre"] == "Sócrates el Grande"
        assert data["epoca"] == "Clásica"

    @pytest.mark.unit
    def test_update_author_not_found(self, client):
        """Test actualizar autor inexistente."""
        update_data = {"nombre": "Test"}
        response = client.put("/authors/99999", json=update_data)
        assert response.status_code == 404

    @pytest.mark.unit
    def test_delete_author_success(self, client, sample_author):
        """Test eliminar un autor."""
        response = client.delete(f"/authors/{sample_author.id}")
        assert response.status_code == 204

        # Verificar que el autor ya no existe
        response = client.get(f"/authors/{sample_author.id}")
        assert response.status_code == 404

    @pytest.mark.unit
    def test_delete_author_not_found(self, client):
        """Test eliminar autor inexistente."""
        response = client.delete("/authors/99999")
        assert response.status_code == 404

    @pytest.mark.unit
    def test_list_author_schools(self, client, sample_author, sample_school, db_session):
        """Test listar escuelas de un autor."""
        # Asociar autor con escuela
        sample_author.schools.append(sample_school)
        db_session.commit()

        response = client.get(f"/authors/{sample_author.id}/schools")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["nombre"] == "Estoicismo"

    @pytest.mark.unit
    def test_list_author_schools_not_found(self, client):
        """Test listar escuelas de autor inexistente."""
        response = client.get("/authors/99999/schools")
        assert response.status_code == 404

    @pytest.mark.unit
    def test_link_author_school_success(self, client, sample_author, sample_school):
        """Test vincular autor con escuela."""
        response = client.post(f"/authors/{sample_author.id}/schools/{sample_school.id}")
        assert response.status_code == 204

        # Verificar la vinculación
        response = client.get(f"/authors/{sample_author.id}/schools")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["id"] == sample_school.id

    @pytest.mark.unit
    def test_link_author_school_author_not_found(self, client, sample_school):
        """Test vincular autor inexistente con escuela."""
        response = client.post(f"/authors/99999/schools/{sample_school.id}")
        assert response.status_code == 404
        assert "Autor no encontrado" in response.json()["detail"]

    @pytest.mark.unit
    def test_link_author_school_school_not_found(self, client, sample_author):
        """Test vincular autor con escuela inexistente."""
        response = client.post(f"/authors/{sample_author.id}/schools/99999")
        assert response.status_code == 404
        assert "Escuela no encontrada" in response.json()["detail"]

    @pytest.mark.unit
    def test_unlink_author_school_success(self, client, sample_author, sample_school, db_session):
        """Test desvincular autor de escuela."""
        # Primero vincular
        sample_author.schools.append(sample_school)
        db_session.commit()

        # Desvincular
        response = client.delete(f"/authors/{sample_author.id}/schools/{sample_school.id}")
        assert response.status_code == 204

        # Verificar desvinculación
        response = client.get(f"/authors/{sample_author.id}/schools")
        assert response.status_code == 200
        assert response.json() == []

    @pytest.mark.unit
    def test_list_author_books(self, client, sample_author, sample_book):
        """Test listar libros de un autor."""
        response = client.get(f"/authors/{sample_author.id}/books")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["titulo"] == "Apología de Sócrates"

    @pytest.mark.unit
    def test_list_author_quotes(self, client, sample_author, sample_quote):
        """Test listar citas de un autor."""
        response = client.get(f"/authors/{sample_author.id}/quotes")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["texto"] == "Solo sé que no sé nada"


class TestAuthorsIntegration:
    """Tests de integración para el router de authors."""

    @pytest.mark.integration
    def test_full_author_workflow(self, client, db_session):
        """Test flujo completo de manejo de autores."""
        # 1. Crear autor
        author_data = {
            "nombre": "Friedrich Nietzsche", 
            "epoca": "Moderna",
            "biografia": "Filósofo alemán"
        }
        response = client.post("/authors/", json=author_data)
        assert response.status_code == 201
        author_id = response.json()["id"]

        # 2. Obtener autor creado
        response = client.get(f"/authors/{author_id}")
        assert response.status_code == 200
        assert response.json()["nombre"] == "Friedrich Nietzsche"

        # 3. Crear escuela
        school_data = {
            "nombre": "Existencialismo",
            "descripcion": "Corriente filosófica"
        }
        response = client.post("/schools/", json=school_data)
        school_id = response.json()["id"]

        # 4. Vincular autor con escuela
        response = client.post(f"/authors/{author_id}/schools/{school_id}")
        assert response.status_code == 204

        # 5. Verificar vinculación
        response = client.get(f"/authors/{author_id}")
        data = response.json()
        assert len(data["schools"]) == 1
        assert data["schools"][0]["nombre"] == "Existencialismo"

        # 6. Actualizar autor
        update_data = {
            "nombre": "Friedrich Wilhelm Nietzsche",
            "epoca": "Contemporánea",
            "biografia": "Filósofo alemán del siglo XIX"
        }
        response = client.put(f"/authors/{author_id}", json=update_data)
        assert response.status_code == 200
        assert response.json()["nombre"] == "Friedrich Wilhelm Nietzsche"

        # 7. Eliminar autor
        response = client.delete(f"/authors/{author_id}")
        assert response.status_code == 204

        # 8. Verificar eliminación
        response = client.get(f"/authors/{author_id}")
        assert response.status_code == 404