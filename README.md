# 🏛️ Pirate Philosopher

Aplicación web moderna para explorar filosofía a través de autores, escuelas, libros y citas.

## 🚧 Migración a Serverless

**Estado:** En proceso de migración de EC2/RDS a arquitectura serverless

### Migración planificada:
- **Backend FastAPI** → **AWS Lambda + API Gateway**
- **PostgreSQL RDS** → **RDS Serverless v2** 
- **EC2 + Docker** → **Vercel/Netlify**
- **Costo:** $5.82/mes → $3-6/mes (solo por uso)

*Demo estará disponible tras completar la migración*

## ✨ Datos

- **114 Filósofos** con biografías completas
- **85 Escuelas** filosóficas
- **691 Citas** verificadas  
- **188 Libros** y audiolibros

## 🧠 Roadmap

| Fase | Estado |
|------|--------|
| 🧱 **Base de datos completa** | ✅ **Completado** |
| 📚 **API REST robusta** | ✅ **Completado** |
| 🎨 **Frontend moderno** | ✅ **Completado** |
| 🔍 Indexación semántica | 🔄 En progreso |
| 🤖 Integración LLM | 🔜 Próximo |
| 🧠 RAG | 🔜 Próximo |

## 🛠️ Stack

**Frontend:** Next.js 14, TypeScript, Tailwind CSS  
**Backend:** FastAPI, SQLAlchemy, PostgreSQL  
**DevOps:** Docker Compose

## 🚀 Uso

```bash
git clone <repo>
cd cursor-filosofea
docker-compose up -d
```

**URLs:**
- Frontend: http://localhost:3000  
- API: http://localhost:8000/docs

Los datos se cargan automáticamente al iniciar.