# 🏛️ Filosofía App

Aplicación web moderna para explorar la filosofía a través de autores, escuelas, libros y citas inspiradoras.

## ✨ Características

- **91 Filósofos** con biografías detalladas y épocas correctas
- **30+ Escuelas** filosóficas con descripciones
- **Imágenes reales** extraídas de Wikipedia + S3
- **Búsqueda y paginación** optimizada (50 autores por página)
- **Interfaz responsive** con Tailwind CSS

## 🛠️ Stack

**Frontend:** Next.js 14, TypeScript, Tailwind CSS  
**Backend:** FastAPI, SQLAlchemy, PostgreSQL  
**DevOps:** Docker, Terraform, GitHub Actions  
**AWS:** EC2, RDS, S3, CloudFront (Free Tier)

## 🚀 Quick Start

```bash
# Desarrollo local
git clone https://github.com/enriquemorenogonzalez90/Pirate-philosopher-app.git
docker-compose up -d

# URLs
# Frontend: http://localhost:3000
# Backend: http://localhost:8000/docs
```

```bash
# Deployment AWS
./deploy-terraform.sh apply
./deploy-terraform.sh outputs
```

## 📁 Estructura

```
├── frontend/          # Next.js app
├── backend/           # FastAPI + PostgreSQL
│   ├── app/           # Core application
│   ├── biography_data.py    # 99 detailed biographies
│   └── *.py           # Utility scripts
├── terraform/         # AWS infrastructure
└── CLAUDE.md         # Development guide
```

## 🔧 Scripts Disponibles

- **Biografías:** `update_biographies.py`, `check_biography_progress.py`
- **Imágenes:** `better_image_script.py`, `force_regenerate_images.py`
- **Limpieza:** `remove_*.py`, `verify_removal.py`
- **Debug:** `debug_dates.py`, `check_authors.py`

---

**Desarrollado con ❤️ para expandir el conocimiento filosófico**
