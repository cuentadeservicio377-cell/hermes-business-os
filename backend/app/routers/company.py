"""
Company configuration endpoints
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.database import get_db
from core.config import client_config
from models.company import Company, Department

router = APIRouter()


@router.get("/company")
async def get_company(db: Session = Depends(get_db)):
    """Get current company configuration."""
    return {
        "config": client_config._config,
        "departments": [
            {
                "name": d.get("name"),
                "enabled": d.get("enabled"),
                "skills": d.get("skills", [])
            }
            for d in client_config.departments
        ]
    }


@router.get("/company/departments/{name}")
async def get_department(name: str):
    """Get specific department configuration."""
    dept = client_config.get_department(name)
    if not dept:
        return {"error": f"Department '{name}' not found"}
    return dept
