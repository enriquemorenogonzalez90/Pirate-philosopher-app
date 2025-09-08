"""
FastAPI app optimized for Google Cloud Run
"""
import os
from typing import List

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import authors_gcp, books_gcp, schools_gcp, quotes_gcp, stats_gcp


def get_cors_origins_from_env() -> List[str]:
    """Get CORS origins from environment variables"""
    raw = os.getenv("CORS_ORIGINS", "*")
    origins = [o.strip() for o in raw.split(",") if o.strip()]
    return origins


# Create FastAPI app
app = FastAPI(
    title="Filosofía App API - Serverless",
    version="2.0.0",
    description="Philosophy app API running on Google Cloud Run + Firestore"
)

# CORS configuration
origins = get_cors_origins_from_env()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins if origins != ["*"] else [
        "http://localhost:3000",                    # Local development
        "https://filosofia-app.vercel.app",         # Production frontend  
        "https://*.vercel.app",                     # Vercel preview deployments
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Include routers
app.include_router(authors_gcp.router)
app.include_router(books_gcp.router) 
app.include_router(schools_gcp.router)
app.include_router(quotes_gcp.router)
app.include_router(stats_gcp.router)


@app.get("/")
def read_root():
    """Root endpoint"""
    return {
        "message": "Filosofía App API - Serverless Edition",
        "version": "2.0.0",
        "database": "Firestore",
        "platform": "Google Cloud Run"
    }


@app.get("/health", tags=["health"])
def healthcheck():
    """Health check endpoint"""
    return {
        "status": "ok",
        "platform": "cloud-run",
        "database": "firestore"
    }


# Entry point for Cloud Run
# The app is started by start.py which uses uvicorn