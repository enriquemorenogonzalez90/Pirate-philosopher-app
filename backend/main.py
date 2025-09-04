"""
Cloud Functions entry point for Filosofía App API

This module provides the entry point for Google Cloud Functions
using the functions-framework approach.
"""

# Import FastAPI app
from app.main_gcp import app

# For Cloud Functions deployment, we need to expose the FastAPI app
# functions-framework will automatically handle the ASGI conversion