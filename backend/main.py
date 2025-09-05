"""
Cloud Functions entry point for Filosofía App API

This module provides the entry point for Google Cloud Functions Gen2
using the functions-framework approach.
"""

# Import FastAPI app
from app.main_gcp import app

# For Cloud Functions deployment with --gen2 flag
# functions-framework will automatically handle the ASGI conversion
# The entry point is 'app' which refers to the FastAPI instance