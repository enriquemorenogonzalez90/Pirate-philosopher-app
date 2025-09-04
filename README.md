# 🏛️ Pirate Philosopher

Aplicación web moderna para explorar filosofía a través de autores, escuelas filosóficas, libros y citas inspiradoras.

## 🌟 Estado Actual

**Arquitectura:** Completamente migrado a **GCP Serverless + Firestore**

- ✅ **Backend:** FastAPI en Google Cloud Functions
- ✅ **Database:** Google Firestore (NoSQL)
- ✅ **Frontend:** Next.js 14 con TypeScript
- ✅ **Infraestructura:** Terraform para GCP

## ✨ Contenido

- **200+ Filósofos** con biografías completas
- **20+ Escuelas** filosóficas históricas
- **182 Libros** con títulos reales de LibriVox
- **60+ Citas** inspiradoras verificadas

## 🛠️ Stack Tecnológico

**Frontend:**
- Next.js 14 con App Router
- TypeScript & Tailwind CSS
- Server-Side Rendering optimizado

**Backend:**
- FastAPI (Python) optimizado para Cloud Functions
- Google Firestore como base de datos NoSQL
- Pydantic para validación de datos

**Infraestructura:**
- Google Cloud Functions (Serverless)
- Google Firestore (Database)
- Terraform para Infrastructure as Code

## 🚀 Desarrollo Local

### Prerequisitos
- Docker & Docker Compose
- Node.js 18+ (para frontend)
- Google Cloud credentials configuradas

### Quick Start

```bash
# Clonar repositorio
git clone https://github.com/tu-usuario/pirate-philosopher
cd pirate-philosopher

# Configurar variables de entorno
cp .env.gcp .env.gcp.local
# Editar .env.gcp.local con tus configuraciones

# Levantar backend (Docker)
docker-compose -f docker-compose-gcp.yml up -d backend

# Levantar frontend (local)
cd frontend
npm install
npm run dev
```

### URLs de Desarrollo
- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs

## 📚 Características

- **🔍 Búsqueda** de filósofos por nombre y época
- **📖 Catálogo** de libros con enlaces a audiolibros
- **🏛️ Escuelas** filosóficas con sus representantes
- **💬 Citas** inspiradoras categorizadas
- **📱 Responsive** optimizado para móvil
- **⚡ Performance** con SSR y optimizaciones Next.js

## 🚧 Roadmap

| Característica | Estado |
|---------------|--------|
| 🧱 **Base de datos Firestore** | ✅ **Completado** |
| 📚 **API REST completa** | ✅ **Completado** |
| 🎨 **Frontend moderno** | ✅ **Completado** |
| 🔍 **Búsqueda avanzada** | 🔄 En progreso |
| 🤖 **Integración IA** | 🔜 Próximo |
| 🌐 **PWA** | 🔜 Próximo |

## 📄 Documentación

La documentación técnica completa está disponible en:
- **CLAUDE.md** - Guía técnica detallada para desarrollo
- **API Docs** - http://localhost:8000/docs (cuando ejecutes el backend)

## 🤝 Contribuir

1. Fork el repositorio
2. Crear rama feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit cambios (`git commit -m 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abrir Pull Request

## 📜 Licencia

Este proyecto está bajo la Licencia MIT. Ver `LICENSE` para más detalles.

---

*Desarrollado con ❤️ para democratizar el acceso al conocimiento filosófico*