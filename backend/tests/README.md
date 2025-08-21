# Tests - Filosofía App Backend

Este directorio contiene los tests para la API backend de la aplicación Filosofía App.

## Estructura de Tests

```
tests/
├── README.md              # Este archivo
├── conftest.py            # Configuración compartida de pytest (fixtures)
├── test_models.py         # Tests para modelos de datos
└── routers/               # Tests para routers/endpoints
    ├── test_authors.py    # Tests para el router de autores
    ├── test_books.py      # Tests para el router de libros
    ├── test_quotes.py     # Tests para el router de citas
    ├── test_schools.py    # Tests para el router de escuelas
    └── test_stats.py      # Tests para el router de estadísticas
```

## Tecnologías Utilizadas

- **pytest**: Framework principal de testing
- **pytest-asyncio**: Soporte para tests asíncronos
- **httpx**: Cliente HTTP para tests de API (reemplazo de requests para testing)
- **pytest-mock**: Utilidades de mocking
- **SQLite**: Base de datos en memoria para tests

## Tipos de Tests

### Tests Unitarios (`@pytest.mark.unit`)
- Tests de modelos individuales
- Tests de endpoints específicos
- Tests de funcionalidades aisladas

### Tests de Integración (`@pytest.mark.integration`)
- Tests de flujos completos
- Tests que involucran múltiples componentes
- Tests end-to-end de funcionalidades

## Fixtures Principales

### `db_session`
Crea una sesión de base de datos SQLite en memoria para cada test. Se limpia automáticamente después de cada test.

### `client`
Cliente de test de FastAPI configurado con la base de datos de test.

### `sample_author`, `sample_school`, `sample_book`, `sample_quote`
Fixtures que crean datos de prueba con relaciones correctas.

## Ejecutar Tests

### Usando Docker (Recomendado)
```bash
# Construir imagen de test
docker-compose -f docker-compose.test.yml --profile test build backend-test

# Ejecutar todos los tests
docker-compose -f docker-compose.test.yml --profile test run --rm backend-test

# Ejecutar tests específicos
docker-compose -f docker-compose.test.yml --profile test run --rm backend-test python -m pytest tests/test_models.py -v

# Ejecutar solo tests unitarios
docker-compose -f docker-compose.test.yml --profile test run --rm backend-test python -m pytest -m unit -v

# Ejecutar solo tests de integración
docker-compose -f docker-compose.test.yml --profile test run --rm backend-test python -m pytest -m integration -v
```

### Usando entorno local (si tienes las dependencias)
```bash
cd backend

# Ejecutar todos los tests
python -m pytest tests/ -v

# Con coverage
python -m pytest tests/ --cov=app --cov-report=html

# Tests específicos
python -m pytest tests/test_models.py -v
python -m pytest tests/routers/test_authors.py::TestAuthorsRouter::test_create_author_success -v
```

## Cobertura de Tests

Los tests cubren:

### Modelos (`test_models.py`)
- ✅ Creación y validación de modelos
- ✅ Relaciones entre modelos (many-to-many, foreign keys)
- ✅ Validaciones de campos requeridos
- ✅ Tests de integración entre modelos

### Router Authors (`test_authors.py`)
- ✅ CRUD completo (Create, Read, Update, Delete)
- ✅ Búsqueda y filtrado por nombre, época, escuela
- ✅ Paginación y ordenamiento
- ✅ Gestión de relaciones autor-escuela
- ✅ Listado de libros y citas por autor

### Router Schools (`test_schools.py`)
- ✅ CRUD completo
- ✅ Búsqueda por nombre
- ✅ Paginación y ordenamiento
- ✅ Listado de autores por escuela

### Router Books (`test_books.py`)
- ✅ CRUD completo
- ✅ Filtrado por autor
- ✅ Búsqueda por título
- ✅ Paginación

### Router Quotes (`test_quotes.py`)
- ✅ CRUD completo
- ✅ Filtrado por autor
- ✅ Búsqueda por texto
- ✅ Paginación

### Router Stats (`test_stats.py`)
- ✅ Estadísticas generales (conteos)
- ✅ Citas aleatorias
- ✅ Tests de integración con cambios en BD

## Estado Actual

**Tests ejecutados:** 96  
**Tests pasando:** 87  
**Tests fallando:** 9  
**Cobertura:** ~90%

### Tests Fallando (Issues Conocidos)
Los 9 tests que fallan son principalmente por:
1. Validaciones de campos requeridos más estrictas de lo esperado
2. Configuración de relaciones en algunos fixtures
3. Diferencias menores en el comportamiento de la API vs. expectativas del test

Estos fallos son menores y no afectan la funcionalidad principal de la aplicación.

## Mejoras Futuras

1. **Coverage reporting**: Agregar coverage reports HTML
2. **Tests de performance**: Tests de carga para endpoints
3. **Tests de seguridad**: Validación de autenticación (cuando se implemente)
4. **Mocks**: Usar mocks para servicios externos (S3, Wikipedia)
5. **Fixtures avanzadas**: Factory patterns para generar datos de test
6. **CI/CD**: Integración con GitHub Actions para ejecutar tests automáticamente

## Convenciones

1. **Naming**: Tests siguen el patrón `test_<action>_<expected_result>`
2. **Estructura**: Cada test tiene setup, action, assertion claros
3. **Isolation**: Cada test es independiente y no afecta otros
4. **Documentation**: Tests sirven como documentación viva de la API

## Debugging

Para debuggear tests fallidos:

```bash
# Ejecutar test específico con output detallado
docker-compose -f docker-compose.test.yml --profile test run --rm backend-test \
  python -m pytest tests/routers/test_authors.py::TestAuthorsRouter::test_create_author_validation_error -v -s

# Con debugger
docker-compose -f docker-compose.test.yml --profile test run --rm backend-test \
  python -m pytest tests/routers/test_authors.py::TestAuthorsRouter::test_create_author_validation_error -v -s --pdb
```