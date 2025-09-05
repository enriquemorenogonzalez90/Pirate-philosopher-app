"""
Startup script for Cloud Run deployment
Handles the PORT environment variable dynamically
"""
import os
import uvicorn
from app.main_gcp import app

if __name__ == "__main__":
    # Cloud Run provides PORT environment variable
    port = int(os.environ.get("PORT", 8000))
    
    # Start uvicorn server
    uvicorn.run(
        app,
        host="0.0.0.0", 
        port=port,
        log_level="info"
    )