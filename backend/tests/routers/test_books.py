import pytest
from fastapi.testclient import TestClient

from app.models import Book, Author


class TestBooksRouter:
    """Tests para el router de books."""

    @pytest.mark.unit
    def test_list_books_empty(self, client):
        """Test listar libros cuando no hay ninguno."""
        response = client.get("/books/")
        assert response.status_code == 200
        assert response.json() == []

    @pytest.mark.unit
    def test_list_books_with_data(self, client, sample_book, sample_author):
        """Test listar libros con datos."""
        response = client.get("/books/")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["titulo"] == "Apología de Sócrates"
        assert data[0]["id"] == sample_book.id
        assert data[0]["author"]["nombre"] == "Sócrates"

    @pytest.mark.unit
    def test_list_books_by_author(self, client, sample_book, sample_author, db_session):
        """Test filtrar libros por autor."""
        # Crear otro autor y libro
        other_author = Author(nombre="Platón")
        other_book = Book(titulo="La República", autor_id=other_author.id)
        other_author.books = [other_book]
        db_session.add(other_author)
        db_session.add(other_book)
        db_session.commit()

        # Filtrar por el primer autor
        response = client.get(f"/books/?autor_id={sample_author.id}")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["titulo"] == "Apología de Sócrates"

        # Filtrar por el segundo autor
        response = client.get(f"/books/?autor_id={other_author.id}")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["titulo"] == "La República"

    @pytest.mark.unit
    def test_list_books_with_search(self, client, sample_book):
        """Test búsqueda de libros por título."""
        response = client.get("/books/?q=Apología")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["titulo"] == "Apología de Sócrates"

        # Búsqueda que no encuentra nada
        response = client.get("/books/?q=Inexistente")
        assert response.status_code == 200
        assert response.json() == []

    @pytest.mark.unit
    def test_list_books_pagination(self, client, db_session):
        """Test paginación de libros."""
        # Crear un autor
        author = Author(nombre="Autor Test")
        db_session.add(author)
        db_session.commit()

        # Crear múltiples libros
        for i in range(25):
            book = Book(titulo=f"Libro {i}", autor_id=author.id)
            db_session.add(book)
        db_session.commit()

        # Test primer página
        response = client.get("/books/?limit=10&offset=0")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 10

        # Test segunda página
        response = client.get("/books/?limit=10&offset=10")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 10

    @pytest.mark.unit
    def test_get_book_success(self, client, sample_book):
        """Test obtener un libro específico."""
        response = client.get(f"/books/{sample_book.id}")
        assert response.status_code == 200
        data = response.json()
        assert data["titulo"] == "Apología de Sócrates"
        assert data["id"] == sample_book.id

    @pytest.mark.unit
    def test_get_book_not_found(self, client):
        """Test obtener libro inexistente."""
        response = client.get("/books/99999")
        assert response.status_code == 404
        assert "Libro no encontrado" in response.json()["detail"]

    @pytest.mark.unit
    def test_create_book_success(self, client, sample_author):
        """Test crear un nuevo libro."""
        book_data = {
            "titulo": "Ética a Nicómaco",
            "autor_id": sample_author.id,
            "descripcion": "Obra sobre ética de Aristóteles"
        }
        response = client.post("/books/", json=book_data)
        assert response.status_code == 201
        data = response.json()
        assert data["titulo"] == "Ética a Nicómaco"
        assert data["autor_id"] == sample_author.id
        assert "id" in data

    @pytest.mark.unit
    def test_create_book_validation_error(self, client):
        """Test crear libro con datos inválidos."""
        # Datos faltantes (titulo y autor_id son requeridos)
        response = client.post("/books/", json={})
        assert response.status_code == 422

        # Solo título sin autor
        response = client.post("/books/", json={"titulo": "Libro Test"})
        assert response.status_code == 422

        # Solo autor sin título
        response = client.post("/books/", json={"autor_id": 1})
        assert response.status_code == 422

    @pytest.mark.unit
    def test_create_book_with_nonexistent_author(self, client):
        """Test crear libro con autor inexistente."""
        book_data = {
            "titulo": "Libro Test",
            "autor_id": 99999
        }
        response = client.post("/books/", json=book_data)
        # La API permite crear el libro pero la relación será inválida
        # En un sistema más robusto, esto debería validar la existencia del autor
        assert response.status_code == 201

    @pytest.mark.unit
    def test_update_book_success(self, client, sample_book):
        """Test actualizar un libro."""
        update_data = {
            "titulo": "Apología de Sócrates - Edición Revisada",
            "autor_id": sample_book.autor_id,
            "descripcion": "Descripción actualizada"
        }
        response = client.put(f"/books/{sample_book.id}", json=update_data)
        assert response.status_code == 200
        data = response.json()
        assert data["titulo"] == "Apología de Sócrates - Edición Revisada"
        assert data["descripcion"] == "Descripción actualizada"

    @pytest.mark.unit
    def test_update_book_not_found(self, client, sample_author):
        """Test actualizar libro inexistente."""
        update_data = {
            "titulo": "Test",
            "autor_id": sample_author.id
        }
        response = client.put("/books/99999", json=update_data)
        assert response.status_code == 404

    @pytest.mark.unit
    def test_delete_book_success(self, client, sample_book):
        """Test eliminar un libro."""
        response = client.delete(f"/books/{sample_book.id}")
        assert response.status_code == 204

        # Verificar que el libro ya no existe
        response = client.get(f"/books/{sample_book.id}")
        assert response.status_code == 404

    @pytest.mark.unit
    def test_delete_book_not_found(self, client):
        """Test eliminar libro inexistente."""
        response = client.delete("/books/99999")
        assert response.status_code == 404


class TestBooksIntegration:
    """Tests de integración para el router de books."""

    @pytest.mark.integration
    def test_full_book_workflow(self, client):
        """Test flujo completo de manejo de libros."""
        # 1. Crear autor
        author_data = {
            "nombre": "Marcus Aurelius",
            "epoca": "Antigua"
        }
        response = client.post("/authors/", json=author_data)
        assert response.status_code == 201
        author_id = response.json()["id"]

        # 2. Crear libro
        book_data = {
            "titulo": "Meditaciones",
            "autor_id": author_id,
            "descripcion": "Reflexiones personales del emperador filósofo"
        }
        response = client.post("/books/", json=book_data)
        assert response.status_code == 201
        book_id = response.json()["id"]

        # 3. Obtener libro creado
        response = client.get(f"/books/{book_id}")
        assert response.status_code == 200
        assert response.json()["titulo"] == "Meditaciones"

        # 4. Verificar que aparece en la lista de libros
        response = client.get("/books/")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["titulo"] == "Meditaciones"
        assert data[0]["author"]["nombre"] == "Marcus Aurelius"

        # 5. Verificar filtrado por autor
        response = client.get(f"/books/?autor_id={author_id}")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["titulo"] == "Meditaciones"

        # 6. Actualizar libro
        update_data = {
            "titulo": "Meditaciones - Edición Completa",
            "autor_id": author_id,
            "descripcion": "Edición completa de las reflexiones"
        }
        response = client.put(f"/books/{book_id}", json=update_data)
        assert response.status_code == 200
        assert response.json()["titulo"] == "Meditaciones - Edición Completa"

        # 7. Eliminar libro
        response = client.delete(f"/books/{book_id}")
        assert response.status_code == 204

        # 8. Verificar eliminación
        response = client.get(f"/books/{book_id}")
        assert response.status_code == 404

    @pytest.mark.integration
    def test_books_search_and_filtering(self, client, db_session):
        """Test búsqueda y filtrado avanzado de libros."""
        # Crear autores
        author1 = Author(nombre="Aristóteles")
        author2 = Author(nombre="Platón")
        db_session.add(author1)
        db_session.add(author2)
        db_session.commit()

        # Crear libros
        books = [
            Book(titulo="Ética a Nicómaco", autor_id=author1.id),
            Book(titulo="Política", autor_id=author1.id),
            Book(titulo="La República", autor_id=author2.id),
            Book(titulo="Fedro", autor_id=author2.id)
        ]
        
        for book in books:
            db_session.add(book)
        db_session.commit()

        # Test búsqueda por título parcial
        response = client.get("/books/?q=Ética")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["titulo"] == "Ética a Nicómaco"

        # Test filtrado por autor
        response = client.get(f"/books/?autor_id={author1.id}")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        titles = [book["titulo"] for book in data]
        assert "Ética a Nicómaco" in titles
        assert "Política" in titles

        # Test paginación
        response = client.get("/books/?limit=2")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2