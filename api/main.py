"""
FastAPI application for Student Loan Document Extractor Platform
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Student Loan Document Extractor API",
    description="API for extracting and analyzing student loan documents",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Student Loan Document Extractor API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "api"
    }


@app.get("/api/v1/status")
async def api_status():
    """API status endpoint"""
    return {
        "api": "online",
        "database": "connected",  # TODO: Add actual DB check
        "storage": "connected"     # TODO: Add actual storage check
    }


# Import routes if they exist
try:
    from api.routes import router
    app.include_router(router, prefix="/api/v1")
    logger.info("API routes loaded successfully")
except ImportError as e:
    logger.warning(f"Could not load API routes: {e}")


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("API_PORT", "8000"))
    uvicorn.run(app, host="0.0.0.0", port=port)
