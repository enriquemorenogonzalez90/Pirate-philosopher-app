# 🏴‍☠️ Pirate Philosopher

Una aplicación web completa para la gestión y exploración de una biblioteca de filosofía. Desarrollada con tecnologías modernas y diseño responsive.

## 🚀 Características Principales

### 📚 Gestión de Contenido Filosófico
- **Autores**: Biografías detalladas, fechas de nacimiento/muerte, retratos reales
- **Escuelas Filosóficas**: Descripciones académicas e imágenes representativas  
- **Libros**: Títulos reales con portadas de Open Library API
- **Citas**: Sistema de citas aleatorias con rotación automática

### 🎨 Interfaz de Usuario
- **Diseño Responsive**: Funciona perfectamente en móvil y desktop
- **Tailwind CSS**: Diseño moderno y consistente
- **Navegación Intuitiva**: Enlaces cruzados entre autores, escuelas y obras
- **Paginación**: Cliente y servidor para manejo eficiente de datos

### 🔧 Tecnologías

#### Backend
- **FastAPI**: Framework web moderno y rápido
- **SQLAlchemy 2.0**: ORM avanzado con tipos Mapped
- **Pydantic 2.x**: Validación y serialización de datos
- **PostgreSQL**: Base de datos relacional robusta
- **Docker**: Contenedorización para desarrollo y producción

#### Frontend
- **Next.js 14**: Framework React con App Router
- **TypeScript**: Tipado estático para mayor confiabilidad
- **Tailwind CSS**: Framework CSS utility-first
- **Client-side Pagination**: Navegación fluida de contenido

## 🐳 Configuración y Ejecución

### Prerrequisitos
- Docker y Docker Compose
- Git

### Instalación

1. **Clonar el repositorio**
```bash
git clone <repository-url>
cd cursor-filosofea
```

2. **Ejecutar con Docker Compose**
```bash
docker compose up --build
```

3. **Acceder a la aplicación**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- Documentación API: http://localhost:8000/docs

### Desarrollo Local

#### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend
```bash
cd frontend
npm install
npm run dev
```

## 📊 Estructura del Proyecto

```
cursor-filosofea/
├── backend/                 # API FastAPI
│   ├── app/
│   │   ├── routers/        # Endpoints organizados por entidad
│   │   ├── models.py       # Modelos SQLAlchemy
│   │   ├── schemas.py      # Esquemas Pydantic
│   │   ├── database.py     # Configuración de BD
│   │   ├── seed.py         # Datos iniciales
│   │   └── main.py         # Aplicación principal
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/                # Aplicación Next.js
│   ├── src/app/
│   │   ├── authors/        # Páginas de autores
│   │   ├── schools/        # Páginas de escuelas
│   │   ├── books/          # Páginas de libros
│   │   ├── quotes/         # Páginas de citas
│   │   └── globals.css     # Estilos globales
│   ├── Dockerfile
│   └── package.json
└── docker-compose.yml      # Orquestación de servicios
```

## 🔗 API Endpoints

### Autores
- `GET /authors/` - Listar autores con paginación
- `GET /authors/{id}` - Detalle de autor con relaciones
- `GET /authors/{id}/books` - Libros del autor
- `GET /authors/{id}/quotes` - Citas del autor

### Escuelas
- `GET /schools/` - Listar escuelas
- `GET /schools/{id}` - Detalle de escuela con autores

### Libros y Citas
- `GET /books/` - Listar libros con portadas
- `GET /quotes/` - Listar citas
- `GET /random-quotes` - Citas aleatorias para homepage

### Estadísticas
- `GET /stats/` - Estadísticas generales del sistema

## 🎯 Características Técnicas Destacadas

### Backend
- **Migración SQLModel → SQLAlchemy 2.0**: Mayor estabilidad y control
- **Retratos Reales**: Integración con Wikipedia API para imágenes de autores
- **Portadas de Libros**: Open Library API para covers auténticas
- **Datos Académicos**: Biografías detalladas y fechas históricas precisas
- **Relationships Optimizadas**: Eager loading para mejor rendimiento

### Frontend
- **Dynamic Rendering**: Evita problemas de hidratación con SSR
- **Error Boundaries**: Manejo robusto de errores de imágenes
- **Responsive Grid**: Layouts adaptativos para diferentes dispositivos
- **Type Safety**: TypeScript en toda la aplicación

## 🎨 Diseño y UX

- **Tema Pirata**: Colores y nomenclatura temática
- **Cards Modernas**: Layout tipo tarjeta para mejor organización
- **Hover Effects**: Transiciones suaves para mejor interactividad
- **Loading States**: Indicadores de carga para mejor UX
- **Fallback Images**: Avatares generados dinámicamente cuando fallan las imágenes

## 📈 Próximas Mejoras

- [ ] Sistema de búsqueda avanzada
- [ ] Favoritos y listas personalizadas
- [ ] Comentarios y reseñas de libros
- [ ] Integración con más APIs de libros
- [ ] PWA (Progressive Web App)
- [ ] Modo oscuro
- [ ] Internacionalización (i18n)

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una branch de feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -am 'Añadir nueva funcionalidad'`)
4. Push a la branch (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

---

**Desarrollado con ❤️ para la comunidad filosófica** 🏴‍☠️📚
