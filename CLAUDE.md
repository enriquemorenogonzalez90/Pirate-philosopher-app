# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is "Filosofía App" - a modern web application for exploring philosophy through authors, philosophical schools, books, and inspirational quotes. It's a full-stack application with React/Next.js frontend and FastAPI/PostgreSQL backend, designed to run on AWS Free Tier.

## Architecture

### Frontend (`/frontend/`)
- **Next.js 14** with TypeScript
- **Tailwind CSS** for styling
- Server-side rendering and static generation
- Responsive design for mobile and desktop

### Backend (`/backend/`)
- **FastAPI** Python framework
- **SQLAlchemy** ORM with PostgreSQL
- **Pydantic** for data validation
- RESTful API with automatic OpenAPI documentation
- Routers organized by entity: authors, books, schools, quotes, stats

### Database Models
Core entities in `backend/app/models.py`:
- Authors (philosophers with biographies)
- Schools (philosophical schools of thought)
- Books (philosophical works)
- Quotes (inspirational quotes from philosophers)

### Image Management
- Wikipedia image extraction (`backend/app/wikipedia_images.py`)
- AWS S3 integration (`backend/app/aws_s3.py`)
- Automated image scripts in `backend/` root

## Common Development Commands

### Local Development
```bash
# Start full stack with Docker Compose
docker-compose up -d

# Frontend only (from /frontend/)
npm run dev          # Development server (localhost:3000)
npm run build        # Production build
npm run start        # Start production build

# Backend only (from /backend/)
uvicorn app.main:app --reload --port 8000
```

### URLs
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

### Production Deployment
```bash
# Deploy to AWS using Terraform
./deploy-terraform.sh apply

# View production URLs
./deploy-terraform.sh outputs
```

## Database Operations

### Seeding Data
Data seeding happens automatically on backend startup via `backend/app/seed.py`. The seed includes:
- 40+ philosophers with biographical data
- 20+ philosophical schools
- 70+ classic and contemporary books
- 60+ inspirational quotes

### Image Management Scripts
```bash
# From backend/ directory
python better_image_script.py          # Improved image processing
python force_regenerate_images.py      # Force regenerate all images
```

## Key Configuration Files

### Environment Setup
- `env.example` - Template for environment variables
- `env.production` - Production environment configuration
- Frontend uses `NEXT_PUBLIC_API_URL` for backend communication
- Backend uses `DATABASE_URL` for PostgreSQL connection

### Docker Configuration
- `docker-compose.yml` - Local development
- `docker-compose.prod.yml` - Production deployment
- Individual Dockerfiles in frontend/ and backend/

### Infrastructure
- `terraform/` - Complete AWS infrastructure as code
- Optimized for AWS Free Tier resources
- Includes EC2, RDS, S3, and CloudFront setup

## Development Notes

### API Structure
The backend follows a clean router-based architecture:
- `/authors` - Philosopher management with pagination (50 per page, 200 total)
- `/books` - Book catalog with author relationships
- `/schools` - Philosophical schools with member relationships
- `/quotes` - Quote collection with author attribution
- `/stats` - Application statistics and metrics

### Frontend Routing
- `/` - Homepage
- `/authors` - Authors listing with pagination
- `/authors/[id]` - Individual author page with books and quotes
- `/schools` - Schools listing
- `/schools/[id]` - Individual school page
- `/books` - Books catalog
- `/quotes` - Quotes collection

### CORS Configuration
CORS is configured in `backend/app/main.py` to allow frontend communication. Currently set to allow all origins for development - should be restricted in production.

### Database Migrations
No formal migration system is implemented. Database schema changes are handled through SQLAlchemy model updates and manual database resets if needed.