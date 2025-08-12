# 🏛️ Filosofía App

Una aplicación web moderna para explorar la filosofía a través de autores, escuelas de pensamiento, libros y citas inspiradoras.

## 🚀 Características

- **40+ Filósofos** con biografías detalladas
- **20+ Escuelas** filosóficas documentadas  
- **70+ Libros** clásicos y contemporáneos
- **60+ Citas** inspiradoras y reflexivas
- **Búsqueda avanzada** por autor, escuela o época
- **Interfaz moderna** con React y Next.js
- **API robusta** con FastAPI y PostgreSQL

## 🛠️ Stack Tecnológico

### Frontend
- **Next.js 13** - Framework React
- **TypeScript** - Tipado estático
- **Tailwind CSS** - Estilos utilitarios
- **Responsive Design** - Móvil y desktop

### Backend  
- **FastAPI** - Framework Python moderno
- **SQLAlchemy** - ORM para base de datos
- **PostgreSQL** - Base de datos relacional
- **Pydantic** - Validación de datos

### DevOps
- **Docker** - Contenedores
- **Docker Compose** - Orquestación local
- **Terraform** - Infrastructure as Code
- **GitHub Actions** - CI/CD automático

## 🆓 Deployment AWS Free Tier

La aplicación está optimizada para desplegarse en AWS usando **exclusivamente recursos del Free Tier** - **$0.00 de costo**.

### Recursos AWS (Gratis por 12 meses)
- **EC2 t2.micro** - Servidor de aplicación
- **RDS db.t2.micro** - Base de datos PostgreSQL  
- **S3 5GB** - Almacenamiento de imágenes
- **CloudFront** - CDN global

## 🚀 Quick Start

### Desarrollo Local

```bash
# Clonar repositorio
git clone https://github.com/balladOfAThinMan/Pirate-philosopher-app.git
cd filosofia-app

# Iniciar con Docker Compose
docker-compose up -d

# URLs locales
# Frontend: http://localhost:3000
# Backend: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### Deployment AWS

```bash
# Prerequisitos
aws configure
terraform --version

# Deployment automático
./deploy-terraform.sh apply

# Ver URLs de producción
./deploy-terraform.sh outputs
```

## 📚 Documentación

- [🏗️ Terraform Setup](terraform/README.md) - Deployment AWS completo
- [🐳 Docker Guide](docs/docker.md) - Desarrollo local
- [🔧 API Documentation](docs/api.md) - Endpoints y schemas

## 🤝 Contribuir

1. Fork el proyecto
2. Crea tu rama (`git checkout -b feature/nueva-caracteristica`)
3. Commit tus cambios (`git commit -am 'Agregar nueva característica'`)
4. Push a la rama (`git push origin feature/nueva-caracteristica`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

## 🎯 Roadmap

- [ ] **Expandir contenido** - 200 autores, 100 escuelas
- [ ] **Modo offline** - PWA con cache
- [ ] **Autenticación** - Favoritos y notas personales
- [ ] **API pública** - Acceso para desarrolladores
- [ ] **Multiidioma** - Español, inglés, francés
- [ ] **Modo oscuro** - Tema personalizable

## 🏆 Características Destacadas

### 🎨 Diseño Moderno
- Interfaz limpia y minimalista
- Navegación intuitiva
- Responsive design para todos los dispositivos

### ⚡ Rendimiento
- Carga rápida con Next.js
- API optimizada con FastAPI
- CDN para imágenes globales

### 🔒 Seguridad
- Validación de datos con Pydantic
- SQL injection protection
- CORS configurado correctamente

### 📊 Datos Ricos
- Biografías detalladas de filósofos
- Contexto histórico de escuelas
- Citas con fuentes verificadas

---

**Desarrollado con ❤️ para expandir el conocimiento filosófico**# Trigger fresh build - mar 12 ago 2025 20:17:03 CEST
