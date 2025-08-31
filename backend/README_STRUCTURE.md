# Estructura Actualizada del Backend

## Estructura de Directorios

```
backend/
├── app/                           # 🎯 Aplicación FastAPI principal
│   ├── __init__.py
│   ├── main.py                    # FastAPI application
│   ├── models/                    # 📊 Modelos y base de datos
│   │   ├── __init__.py
│   │   ├── database.py           # Configuración de SQLAlchemy
│   │   ├── models.py             # Modelos de datos
│   │   └── schemas.py            # Schemas de Pydantic
│   ├── routers/                   # 🛣️ Endpoints de la API
│   │   ├── __init__.py
│   │   ├── authors.py            # Endpoints de autores
│   │   ├── books.py              # Endpoints de libros
│   │   ├── quotes.py             # Endpoints de quotes
│   │   ├── schools.py            # Endpoints de escuelas
│   │   └── stats.py              # Endpoints de estadísticas
│   └── services/                  # 🔧 Servicios externos
│       ├── __init__.py
│       └── aws_s3.py             # Integración con AWS S3
├── data/                          # 📁 Scripts y datos
│   ├── scripts/
│   │   ├── extract_philosophers.py  # Extracción desde API
│   │   └── seed.py               # Seed de base de datos
│   ├── json/                     # Datos JSON extraídos
│   └── cache/                    # Cache temporal
└── tests/                         # 🧪 Tests de la aplicación
```

## Comandos de Uso

### Extracción de Datos

```bash
# Extraer todos los datos desde philosophersapi.com
python3 data/scripts/extract_philosophers.py

# Extraer con límite para prueba
python3 data/scripts/extract_philosophers.py --limit 5 --verbose

# Especificar nombre de archivo personalizado
python3 data/scripts/extract_philosophers.py --output mi_data --verbose
```

### Seed de Base de Datos

```bash
# Ejecutar seed completo (requiere datos extraídos previamente)
python3 data/scripts/seed.py

# Ejecutar en modo verbose
python3 data/scripts/seed.py --verbose
```

### Aplicación FastAPI

```bash
# Ejecutar aplicación en desarrollo
cd app
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# O con Python directo
cd app
python3 -c "import uvicorn; uvicorn.run('main:app', reload=True, host='0.0.0.0', port=8000)"
```

### Docker

```bash
# Construir y ejecutar con docker-compose
docker-compose up -d

# Solo backend
docker-compose up -d backend
```

## Archivos de Configuración

- `requirements.txt` - Dependencias de Python
- `docker-compose.yml` - Configuración de Docker
- `pytest.ini` - Configuración de tests
- `.env` - Variables de entorno (crear basado en .env.example)

## Variables de Entorno Importantes

```bash
# Base de datos
DATABASE_URL=postgresql://user:pass@localhost:5432/filosofia_db

# CORS para el frontend
CORS_ORIGINS=http://localhost:3000,https://mi-frontend.com

# AWS S3 (opcional)
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
AWS_S3_BUCKET=your_bucket
```

## Flujo de Trabajo Recomendado

1. **Extraer datos frescos:**
   ```bash
   python3 data/scripts/extract_philosophers.py
   ```

2. **Poblar base de datos:**
   ```bash
   python3 data/scripts/seed.py --verbose
   ```

3. **Ejecutar aplicación:**
   ```bash
   cd app && uvicorn main:app --reload
   ```

4. **Probar API:**
   - Visitar: http://localhost:8000/docs
   - Health check: http://localhost:8000/health

## Notas Importantes

- Los datos se extraen desde `https://philosophersapi.com/api/philosophers`
- El seed detecta automáticamente duplicados usando `external_id`
- Las imágenes se almacenan en formato JSON con múltiples resoluciones
- Los libros incluyen integración con LibriVox para audiolibros
- Las quotes están mapeadas con sus autores correspondientes