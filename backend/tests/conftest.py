import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import get_session, Base
from app.models import Author, School, Book, Quote


# Base de datos en memoria para tests
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={
        "check_same_thread": False,
    },
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    """Crear una sesión de base de datos para cada test."""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    """Cliente de test de FastAPI con base de datos de test."""
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()
    
    app.dependency_overrides[get_session] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def sample_author(db_session):
    """Crear un autor de ejemplo para tests."""
    author = Author(
        nombre="Sócrates",
        epoca="Antigua", 
        biografia="Filósofo clásico griego considerado como uno de los fundadores de la filosofía occidental.",
        imagen_url="https://example.com/socrates.jpg"
    )
    db_session.add(author)
    db_session.commit()
    db_session.refresh(author)
    return author


@pytest.fixture 
def sample_school(db_session):
    """Crear una escuela filosófica de ejemplo para tests."""
    school = School(
        nombre="Estoicismo",
        descripcion="Escuela filosófica helenística fundada en Atenas",
        imagen_url="https://example.com/stoicism.jpg"
    )
    db_session.add(school)
    db_session.commit() 
    db_session.refresh(school)
    return school


@pytest.fixture
def sample_book(db_session, sample_author):
    """Crear un libro de ejemplo para tests."""
    book = Book(
        titulo="Apología de Sócrates",
        autor_id=sample_author.id,
        descripcion="Diálogo de Platón sobre la defensa de Sócrates",
        imagen_url="https://example.com/book.jpg"
    )
    db_session.add(book)
    db_session.commit()
    db_session.refresh(book)
    return book


@pytest.fixture
def sample_quote(db_session, sample_author):
    """Crear una cita de ejemplo para tests."""
    quote = Quote(
        texto="Solo sé que no sé nada",
        autor_id=sample_author.id
    )
    db_session.add(quote)
    db_session.commit()
    db_session.refresh(quote)
    return quote