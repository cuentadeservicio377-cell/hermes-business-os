"""
Health check endpoint
"""
from fastapi import APIRouter
from core.config import settings, client_config

router = APIRouter()


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "ok",
        "version": settings.APP_VERSION,
        "company": client_config.company.get("name", "Not configured"),
        "departments": [
            d.get("name") for d in client_config.departments if d.get("enabled")
        ]
    }
