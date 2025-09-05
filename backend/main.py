"""
Cloud Functions entry point for Filosofía App API

This module provides the entry point for Google Cloud Functions Gen1.
"""

# Import the FastAPI app
from app.main_gcp import app

# For Cloud Functions Gen1, the entry point should be the FastAPI app instance
# functions-framework will automatically wrap it