# 🚀 Plan de Migración a Arquitectura Serverless

## 📊 Estado Actual
- ✅ **Infraestructura anterior destruida** (EC2 + RDS + S3)
- ✅ **Terraform legacy eliminado** completamente
- ✅ **Costos eliminados**: $5.82/mes → $0.00/mes
- ✅ **Análisis del código completado**:
  - Backend: FastAPI + SQLAlchemy + PostgreSQL
  - Frontend: Next.js 14 + TypeScript + Tailwind CSS
  - Datos: 114 filósofos, 85 escuelas, 691 citas, 188 libros

## 🎯 Objetivo: Arquitectura Serverless
**Costo estimado**: $3-6/mes (solo por uso real vs 24/7 anterior)

## 📋 Pasos de Implementación

### 1. 🏗️ Crear nueva estructura de directorios
```
/serverless/
├── lambda/           # Funciones Lambda (FastAPI + Mangum)
├── infrastructure/   # Terraform serverless config
├── frontend/         # Deployment config (Vercel/Netlify)
└── database/         # RDS Serverless v2 setup
```

### 2. 🔧 Backend: FastAPI → Lambda + API Gateway
- **Adaptar FastAPI con Mangum** para Lambda compatibility
- **Crear funciones Lambda** para cada router:
  - `/authors` - Gestión de filósofos
  - `/books` - Catálogo de libros
  - `/schools` - Escuelas filosóficas
  - `/quotes` - Colección de citas
  - `/stats` - Estadísticas de la app
- **Configurar API Gateway** como proxy
- **Estimated cost**: ~$0.20/mes (Lambda free tier: 1M requests)

### 3. 🗄️ Base de datos: PostgreSQL → RDS Serverless v2
- **Migrar a RDS Serverless v2** (se apaga automáticamente)
- **Configurar auto-scaling** (0.5-16 ACUs)
- **Migrar datos existentes** usando scripts de seed
- **Estimated cost**: ~$2-5/mes (solo cuando activa)

### 4. 🌐 Frontend: Next.js → Vercel/Netlify
- **Deploy en Vercel** o **Netlify** (gratis)
- **Configurar variables de entorno** para nueva API
- **CDN automático** para optimización global
- **Estimated cost**: $0.00/mes

### 5. 🖼️ Almacenamiento: S3 + CloudFront
- **S3 para imágenes** (solo por storage usado)
- **CloudFront CDN** para distribución global
- **Estimated cost**: ~$0.50/mes

### 6. 📦 Infraestructura como Código
- **Nuevo Terraform config** optimizado para serverless
- **Variables de entorno** seguras (AWS Secrets Manager)
- **CI/CD pipeline** con GitHub Actions

## 🔄 Proceso de Migración de Datos
1. **Extraer datos** desde scripts existentes (`backend/data/scripts/`)
2. **Crear nueva RDS Serverless**
3. **Ejecutar seed scripts** en nueva base
4. **Verificar integridad** de datos migrados

## ⚡ Beneficios de la Nueva Arquitectura
- 💰 **Costo reducido**: $5.82/mes → $3-6/mes
- 🔥 **Pago por uso real** (no recursos ociosos 24/7)
- ⚡ **Escalado automático** (0 a millones de requests)
- 🛡️ **Mayor seguridad** (sin servidores expuestos)
- 🚀 **Deploy más rápido** (sin gestión de servidores)
- 🌍 **CDN global** automático
- 🔧 **Mantenimiento mínimo**

## 📝 Notas Técnicas
- **Mangum adapter** permitirá usar FastAPI sin cambios
- **Cold start** inicial ~1-2s (acceptable para esta app)
- **Warm requests** <100ms
- **Free tiers disponibles**: Lambda, API Gateway, S3, CloudFront

## 🚦 Estado Siguiente Sesión
**Empezar por:** Paso 1 - Crear estructura de directorios y configurar Lambda con FastAPI

---
*Actualizado: 2 septiembre 2025*
*Costo anterior eliminado: $5.82/mes*
*Objetivo: Arquitectura serverless $3-6/mes*