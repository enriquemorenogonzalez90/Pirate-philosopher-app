import pytest
from fastapi.testclient import TestClient

from app.models import School, Author


class TestSchoolsRouter:
    """Tests para el router de schools."""

    @pytest.mark.unit
    def test_list_schools_empty(self, client):
        """Test listar escuelas cuando no hay ninguna."""
        response = client.get("/schools/")
        assert response.status_code == 200
        assert response.json() == []

    @pytest.mark.unit
    def test_list_schools_with_data(self, client, sample_school):
        """Test listar escuelas con datos."""
        response = client.get("/schools/")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["nombre"] == "Estoicismo"
        assert data[0]["id"] == sample_school.id

    @pytest.mark.unit
    def test_list_schools_with_search(self, client, sample_school):
        """Test búsqueda de escuelas por nombre."""
        response = client.get("/schools/?q=Estoi")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["nombre"] == "Estoicismo"

        # Búsqueda que no encuentra nada
        response = client.get("/schools/?q=Inexistente")
        assert response.status_code == 200
        assert response.json() == []

    @pytest.mark.unit
    def test_list_schools_pagination(self, client, db_session):
        """Test paginación de escuelas."""
        # Crear múltiples escuelas
        for i in range(25):
            school = School(nombre=f"Escuela {i}")
            db_session.add(school)
        db_session.commit()

        # Test primer página
        response = client.get("/schools/?limit=10&offset=0")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 10

        # Test segunda página
        response = client.get("/schools/?limit=10&offset=10")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 10

    @pytest.mark.unit
    def test_list_schools_sorting(self, client, db_session):
        """Test ordenamiento de escuelas."""
        # Crear escuelas en orden específico
        schools = [
            School(nombre="Zen"),
            School(nombre="Aristotelismo"),
            School(nombre="Budismo")
        ]
        for school in schools:
            db_session.add(school)
        db_session.commit()

        # Test orden ascendente por nombre
        response = client.get("/schools/?sort=nombre")
        assert response.status_code == 200
        data = response.json()
        names = [school["nombre"] for school in data]
        assert names == ["Aristotelismo", "Budismo", "Zen"]

        # Test orden descendente por nombre
        response = client.get("/schools/?sort=-nombre")
        assert response.status_code == 200
        data = response.json()
        names = [school["nombre"] for school in data]
        assert names == ["Zen", "Budismo", "Aristotelismo"]

    @pytest.mark.unit
    def test_get_school_success(self, client, sample_school):
        """Test obtener una escuela específica."""
        response = client.get(f"/schools/{sample_school.id}")
        assert response.status_code == 200
        data = response.json()
        assert data["nombre"] == "Estoicismo"
        assert data["id"] == sample_school.id
        assert "authors" in data

    @pytest.mark.unit
    def test_get_school_not_found(self, client):
        """Test obtener escuela inexistente."""
        response = client.get("/schools/99999")
        assert response.status_code == 404
        assert "Escuela no encontrada" in response.json()["detail"]

    @pytest.mark.unit
    def test_create_school_success(self, client):
        """Test crear una nueva escuela."""
        school_data = {
            "nombre": "Platonismo",
            "descripcion": "Escuela filosófica basada en las ideas de Platón"
        }
        response = client.post("/schools/", json=school_data)
        assert response.status_code == 201
        data = response.json()
        assert data["nombre"] == "Platonismo"
        assert data["descripcion"] == "Escuela filosófica basada en las ideas de Platón"
        assert "id" in data

    @pytest.mark.unit
    def test_create_school_validation_error(self, client):
        """Test crear escuela con datos inválidos."""
        # Datos faltantes (nombre es requerido)
        response = client.post("/schools/", json={})
        assert response.status_code == 422

        # Nombre vacío
        response = client.post("/schools/", json={"nombre": ""})
        assert response.status_code == 422

    @pytest.mark.unit
    def test_update_school_success(self, client, sample_school):
        """Test actualizar una escuela."""
        update_data = {
            "nombre": "Nuevo Estoicismo",
            "descripcion": "Descripción actualizada"
        }
        response = client.put(f"/schools/{sample_school.id}", json=update_data)
        assert response.status_code == 200
        data = response.json()
        assert data["nombre"] == "Nuevo Estoicismo"
        assert data["descripcion"] == "Descripción actualizada"

    @pytest.mark.unit
    def test_update_school_not_found(self, client):
        """Test actualizar escuela inexistente."""
        update_data = {"nombre": "Test"}
        response = client.put("/schools/99999", json=update_data)
        assert response.status_code == 404

    @pytest.mark.unit
    def test_delete_school_success(self, client, sample_school):
        """Test eliminar una escuela."""
        response = client.delete(f"/schools/{sample_school.id}")
        assert response.status_code == 204

        # Verificar que la escuela ya no existe
        response = client.get(f"/schools/{sample_school.id}")
        assert response.status_code == 404

    @pytest.mark.unit
    def test_delete_school_not_found(self, client):
        """Test eliminar escuela inexistente."""
        response = client.delete("/schools/99999")
        assert response.status_code == 404

    @pytest.mark.unit
    def test_list_school_authors(self, client, sample_school, sample_author, db_session):
        """Test listar autores de una escuela."""
        # Asociar escuela con autor
        sample_school.authors.append(sample_author)
        db_session.commit()

        response = client.get(f"/schools/{sample_school.id}/authors")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["nombre"] == "Sócrates"

    @pytest.mark.unit
    def test_list_school_authors_not_found(self, client):
        """Test listar autores de escuela inexistente."""
        response = client.get("/schools/99999/authors")
        assert response.status_code == 404


class TestSchoolsIntegration:
    """Tests de integración para el router de schools."""

    @pytest.mark.integration
    def test_full_school_workflow(self, client):
        """Test flujo completo de manejo de escuelas."""
        # 1. Crear escuela
        school_data = {
            "nombre": "Existencialismo",
            "descripcion": "Corriente filosófica del siglo XX"
        }
        response = client.post("/schools/", json=school_data)
        assert response.status_code == 201
        school_id = response.json()["id"]

        # 2. Obtener escuela creada
        response = client.get(f"/schools/{school_id}")
        assert response.status_code == 200
        assert response.json()["nombre"] == "Existencialismo"

        # 3. Crear autor
        author_data = {
            "nombre": "Jean-Paul Sartre",
            "epoca": "Contemporánea"
        }
        response = client.post("/authors/", json=author_data)
        author_id = response.json()["id"]

        # 4. Vincular autor con escuela
        response = client.post(f"/authors/{author_id}/schools/{school_id}")
        assert response.status_code == 204

        # 5. Verificar vinculación
        response = client.get(f"/schools/{school_id}/authors")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["nombre"] == "Jean-Paul Sartre"

        # 6. Actualizar escuela
        update_data = {
            "nombre": "Existencialismo Francés",
            "descripcion": "Corriente existencialista francesa"
        }
        response = client.put(f"/schools/{school_id}", json=update_data)
        assert response.status_code == 200
        assert response.json()["nombre"] == "Existencialismo Francés"

        # 7. Eliminar escuela
        response = client.delete(f"/schools/{school_id}")
        assert response.status_code == 204

        # 8. Verificar eliminación
        response = client.get(f"/schools/{school_id}")
        assert response.status_code == 404

    @pytest.mark.integration
    def test_school_search_and_filtering(self, client, db_session):
        """Test búsqueda y filtrado avanzado de escuelas."""
        # Crear varias escuelas
        schools = [
            School(nombre="Estoicismo Romano", descripcion="Estoicismo en Roma"),
            School(nombre="Estoicismo Griego", descripcion="Estoicismo en Grecia"),
            School(nombre="Epicureísmo", descripcion="Escuela de Epicuro"),
            School(nombre="Academia", descripcion="Escuela de Platón")
        ]
        
        for school in schools:
            db_session.add(school)
        db_session.commit()

        # Test búsqueda por nombre parcial
        response = client.get("/schools/?q=Esto")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2  # Ambas escuelas estoicas
        
        # Test ordenamiento
        response = client.get("/schools/?sort=nombre")
        assert response.status_code == 200
        data = response.json()
        names = [school["nombre"] for school in data]
        assert names == sorted(names)

        # Test paginación
        response = client.get("/schools/?limit=2")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2